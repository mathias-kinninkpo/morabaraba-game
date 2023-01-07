from math import exp
from core import Color
import random
import numpy as np
from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_action import MorabarabaAction
from morabaraba.morabaraba_action import MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_board import MorabarabaBoard


def count_windows(board,num,player):
    mills = board.mills()
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    c = 0
    for mill in mills:
        if all(adv_piece not in mill for adv_piece in adv_pieces) and len(set(pieces) & set(mill)) == num:
            c+=1
    return c

def get_heuristic(board,player):
    ones = count_windows(board,1,player)
    twos = count_windows(board,2,player)
    threes = count_windows(board,3,player)
    adv_twos = count_windows(board,2,-1*player)
    adv_threes = count_windows(board,3,-1*player)
    score = 1e2*ones + 1e3*twos + 1e7*threes - 1e5*adv_twos - 1e7*adv_threes 
    return score
        
def drop_piece(board,cell,player,act):
    if act == 1:
        board.fill_cell(cell, Color(player))
        if count_windows(board,3,player) > 0:
            return board,True
        return board,False
    return board.empty_cell(cell)
        
        
        
def minimax(board,depth,player,maximizingPlayer,is_steal):
    if depth == 0:
        return get_heuristic(board,player)
    if maximizingPlayer:
        value = -np.Inf
   
        for cell in board.get_all_empty_cells():
            board.fill_cell(cell, Color(player))
            value = max(value, minimax(board,depth-1,player,False,is_steal))
        print(value)
        return value
    else:
        value = np.Inf
       
        for cell in board.get_all_empty_cells():
            board.fill_cell(cell, Color(-1*player))
            value = min(value, minimax(board,depth-1,player,True,is_steal))
        print(value)
        return value
    
    
    

def score_move(board,depth,player,cell):
    board.fill_cell(cell, Color(player))
    score = minimax(board,depth,player,True,False)
    return score
        

def is_making_mill(board,player,cell)  :   
    player_mills = []
    pieces = board.get_player_pieces_on_board(Color(player))
    mills = board.mills()
    for mill in mills:
        if cell in mill: 
            is_mill = True
            for mill_cell in mill:
                if mill_cell not in pieces and mill_cell != cell : is_mill =  False   
            if is_mill == True: 
                 player_mills.append(mill)

    if len(player_mills) == 0: is_player_mill = False 
    else : is_player_mill = True 
    return [ is_player_mill , player_mills ]


def fly(board,player,actions):
    for action in actions:
        if is_making_mill(board,player, action.get_action_as_dict()['action']['to'])[0]:
            return action
    actions = Check_block(actions,board,player)
    for action in actions:
        if is_making_mill(board,-1*player, action.get_action_as_dict()['action']['to'])[0]:
            return action
    occasion = get_occasions(board,player,actions)
    if len(occasion[1]) > 0:
        for action in actions:
            if action.get_action_as_dict()["action"]["to"] == occasion[2][occasion[1].index(max(occasion[1]))]:
                return action
    return False

def is_occasions(board,player):
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    piece_occasions = []
    occasions_mill = []
    for mill in board.mills():
        if all([adv_piece not in mill for adv_piece in adv_pieces]) and len([i for i in set(pieces) & set(mill)]) > 1:
            for mill_cell in mill:
                if mill_cell not in board.get_all_empty_cells():
                    piece_occasions.append(mill_cell)
                    return [True,piece_occasions]
    return [False,[]]
        
def ADD(board,player,actions) :
    acts = []
    for cell in board.get_all_empty_cells() :
        if is_making_mill(board,player,cell)[0]==True:
            for action in actions:
                if action.get_action_as_dict()['action']['to'] == cell:
                    acts.append(action)
    if len(acts) > 0:
        return [True,acts]
    return [False,[]]

def STEAL(board,player,actions) :
    #to check if the opoenent want to do mill
    steal = is_occasions(board,-1*player)
    if steal[0]:
        for piece in steal[1]:
            if any(is_making_mill(board,-1*player,move)[0] for move in get_effective_cell_moves(board,piece)):
                for action in actions:
                    if action.get_action_as_dict()['action']['at'] == piece:
                        print("\ndestroy two occ\n")
                        return action
        occurences = [steal[1].count(i) for i in steal[1]]
        if max(occurences) > 1: 
            for action in actions:
                if action.get_action_as_dict()['action']['at'] == steal[1][occurences.index(max(occurences))]:
                    return action
    for cell in board.get_all_empty_cells() :
        mills=is_making_mill(board,-1*player,cell) 
        if mills[0]==True :
            for mill_cell in mills[1][0] :
                if mill_cell != cell and is_making_mill(board,player,mill_cell)[0]:
                    for action in actions:
                        if action.get_action_as_dict()['action']['at'] == mill_cell :
                            print("\n\n\n\nsteal unknown \n\n\n\n")
                            return action
                elif mill_cell != cell:
                    for action in actions:
                        if action.get_action_as_dict()['action']['at'] == mill_cell :
                            print("\n\n\n\nsteal \n\n\n\n")
                            return action
    occurences = get_occasions(board,-1*player,actions)[1]
    occasions = get_occasions(board,-1*player,actions)[2]
    if len(occurences) > 0 and max(occurences) > 1:
        for mill in board.mills():
            if occasions[occurences.index(max(occurences))] in mill:
                for piece in mill:
                    if piece not in board.get_all_empty_cells():
                        for action in actions:
                            if action.get_action_as_dict()['action']['at'] == piece:
                                print("\n\nc'est fait le steal!! \n")
                                return action  
    occurences = get_occasions(board,player,actions)[1]
    occasions = get_occasions(board,player,actions)[2]
    if len(occurences) > 0 and max(occurences) > 1:
        for mill in board.mills():
            if occasions[occurences.index(max(occurences))] in mill:
                for piece in mill:
                    if piece not in board.get_all_empty_cells():
                        for action in actions:
                            if action.get_action_as_dict()['action']['at'] == piece:
                                print("\n\nc'est fait le steal the mine now !! \n")
                                return action     
    for action in actions:
        for piece in board.get_player_pieces_on_board(Color(player)):
            if is_making_mill(board,player, action.get_action_as_dict()['action']['at'])[0] and any([action.get_action_as_dict()['action']['at'] == move for move in get_effective_cell_moves(board,piece)]):
                print("\n\nmy own steal \n")
                return action                        
            elif is_making_mill(board,player, action.get_action_as_dict()['action']['at'])[0]:
                print("\n\nmy own steal the second else \n")
                return action
        posible_destination = MorabarabaRules.get_rules_possibles_moves(action.get_action_as_dict()['action']['at'],board)
        for mill in player_mill(board,player):
            for piece in posible_destination:
                if piece in mill:
                    print('\nthree my mills\n')
                    return action
        for piece in posible_destination:
            if is_making_mill(board,player,piece) :
                return action
        for piece in posible_destination:
            if piece in board.get_player_pieces_on_board(Color(player)):
                return action
            
    return False 

def get_occasions(board,player,actions):
    good_occasion = []
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    for mill in board.mills():
            for piece in pieces:
                if all([piece in mill and adv_piece not in mill for adv_piece in adv_pieces]):
                    for cell in mill:
                        if cell in board.get_all_empty_cells(): 
                            good_occasion.append(cell)
    if good_occasion:
        occurences = [good_occasion.count(i) for i in good_occasion]
        return [True,occurences,good_occasion]
    return [False,[],[]]
    

def make_occasion_add(board,player, actions):
    good_occasion = []
    opoenent_occasions = []
    opoenent_occurences = []
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    for mill in board.mills():
            for piece in pieces:
                 if all([piece in mill and adv_piece not in mill for adv_piece in adv_pieces]):
                    for cell in mill:
                        if cell in board.get_all_empty_cells(): 
                            good_occasion.append(cell)
    wins = ADD(board,player,actions)
    if wins[0] == True:
        for action in wins[1]:
            if action.get_action_as_dict()['action']['to'] in good_occasion:
                return action
        return wins[1][0]
    blocks = ADD(board,-1*player,actions)
    if blocks[0] == True:
        for action in blocks[1]:
            if action.get_action_as_dict()['action']['to'] in good_occasion:
                return action
        return blocks[1][0]
    if good_occasion:
        occurences = [good_occasion.count(i) for i in good_occasion]
        block = get_occasions(board,-1*player,actions)
        if block[0]:
            opoenent_occasions = block[2]
            opoenent_occurences = block[1]
        if max(occurences) < 2 and len(opoenent_occasions) > 0:
            intersection = [i for i in set(good_occasion) & set(opoenent_occasions)]
            if max(opoenent_occurences) > 1:
                for action in actions:
                    if action.get_action_as_dict()['action']=={'to': opoenent_occasions[opoenent_occurences.index(max(opoenent_occurences))]}:
                        print("\n\nblock two occasions \n")
                        return action
            if len(intersection) > 0:
                occ = [intersection.count(i) for i in intersection]
                for action in actions:
                    if action.get_action_as_dict()['action']=={'to': intersection[occ.index(max(occ))]}:
                        print("\n\nblock occasions\n")
                        return action
        for action in actions:
            if action.get_action_as_dict()['action']=={'to': good_occasion[occurences.index(max(occurences))]}:
                print("\n\ngood occasions \n",max(occurences),"\n")
                return action
        for action in actions:
            if action.get_action_as_dict()['action']=={'to': opoenent_occasions[opoenent_occurences.index(max(opoenent_occurences))]}:
                print("\n\nblock two occasions \n")
                return action
    return False
        
def get_effective_cell_moves(board, cell):
        if board.is_cell_on_board(cell):
            possibles_moves = MorabarabaRules.get_rules_possibles_moves(cell, board)
            effective_moves = []
            for move in possibles_moves:
                if board.is_empty_cell(move):
                    effective_moves.append(move)
            return effective_moves 

def player_mill(board,player):
    p_mills = []
    pieces = board.get_player_pieces_on_board(Color(player))
    for mill in board.mills():
        if mill[0] in pieces and mill[1] in pieces and mill[2] in pieces:
            p_mills.append(mill)
    return p_mills

def Check_Move(state,board,player,actions) :
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill  :
                            print("\n\nwin\n\n")
                            return action
        actions = Check_block(actions, state.get_board(),player)
        adv_actions = MorabarabaRules(-1*player).get_player_actions(state,-1*player)
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,-1*player,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for adv_action in adv_actions:
                        if adv_action.get_action_as_dict()['action']['to'] == cell and adv_action.get_action_as_dict()['action']['at'] not in mill :
                            for action in actions:
                                if action.get_action_as_dict()['action']['to'] == cell:
                                    print("\n\nblock \n\n")
                                    return action
            return False

def choix(state, player, action_pre):
    board = state.get_board()
    possibles_moves = get_effective_cell_moves(board,action_pre.get_action_as_dict()['action']['at'])
    for move in possibles_moves:
        board.empty_cell(action_pre.get_action_as_dict()['action']['at'])
        board.fill_cell(move, Color(player))
        state.set_board(board)
        actions = MorabarabaRules(player).get_player_actions(state,player)
        for cell in board.get_all_empty_cells():
            mills=is_making_mill(board,player,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill and (action.get_action_as_dict()['action']['at'] == move or move in mill):
                            if all([adv_action.get_action_as_dict()['action']['to'] != cell for adv_action in MorabarabaRules(-1*player).get_player_actions(state,-1*player)]):
                                print("\n\nca fait un mill en avant\n")
                                return [True,move] 
                            print('\n\n ca pourait causer de mill en avant\n\n')
                            return [True,1,move]
    return [False,0]
def get_adv_possible_destination(board, player, mill = []):
    adv_possible_destination = []
    for piece in set(board.get_player_pieces_on_board(Color(player))) - set(mill):
        for move in MorabarabaRules.get_rules_possibles_moves(piece,board):
            adv_possible_destination.append(move)
    return adv_possible_destination
    

def create_win(board,player,actions):
    adv_possible_destination = get_adv_possible_destination(board,-1*player)
    for mill in player_mill(board,player):
        for cell in mill:
            for action in actions:
                if action.get_action_as_dict()['action']['at'] == cell:
                    if (all([piece != cell for piece in adv_possible_destination]) and want_to_win(board,-1*player)[0] == False):
                        print("\n\nmill direct\n\n")
                        return [True,action]
    return [False]
def is_block_multiple_mills(board,player,actions):
    for action in actions:
        if any(is_making_mill(board,-1*player,move) for move in MorabarabaRules.get_rules_possibles_moves(action.get_action_as_dict()['action']['to'], board)):
            print("\nblock multiple mills\n")
            return [True,action]
    return [False,[]]
        
def want_to_win(board,player):
    for cell in board.get_all_empty_cells():
        mills = is_making_mill(board,player,cell)
        if mills[0]:
            for mill in mills[1]:
                if any(cell == move for move in  get_adv_possible_destination(board,player,mill)):
                    return [True,mill]
    return [False,[]]
                
def Check_block(actions,board,player):
    for action in actions:
        mills = is_making_mill(board,-1*player,action.get_action_as_dict()['action']['at'])
        if mills[0] == True:
            for mill in mills[1]:
                if any(action.get_action_as_dict()['action']['at'] == move for move in get_adv_possible_destination(board,-1*player,mill)):
                    if len(actions) > 1 and action in actions:
                        print('\n\nRemove Done\n\n')
                        actions.remove(action)
    return actions

def make_occasion_move(board,player,actions):
    posible_destination = [i for i in set(get_adv_possible_destination(board,player)) & set(board.get_all_empty_cells())]
    possible_occasion = get_occasions(board,player,actions)
    for action in actions:
        if action.get_action_as_dict()['action']['to'] in set(posible_destination) & set(possible_occasion[2]):
            print("\nregroupement\n")
            return action
    return False

def play(state, player):

    #try:
    actions = MorabarabaRules(player).get_player_actions(state,player)

    board = state.get_board()

    if len(actions)==0:
        return None
    else:
        if actions[0].get_action_as_dict()['action_type'] == MorabarabaActionType.MOVE:
            action_choice=Check_Move(state,board,player,actions)
            if action_choice != False :
                return action_choice
            actions = Check_block(actions, state.get_board(),player)
            action_choice=Check_Move(state,board,-1*player,actions)
            if action_choice != False :
                return action_choice
            if create_win(state.get_board(),player,actions)[0]:
                return create_win(state.get_board(),player,actions)[1]
            elif action_choice == False:
                # actions = Check_block(actions, state.get_board(),player)
                for action in actions:
                    choice = choix(state, player, action)
                    if choice[0] == True and choice[1] != 1:
                        print("\n\n",choice[1],"\n\n")
                        for action in actions:
                            if action.get_action_as_dict()['action']['to'] == choice[1]:
                                return action
                    elif choice[1] == 1:
                        for action in actions:
                            if  action.get_action_as_dict()['action']['to'] == choice[1]:
                                return action
                if make_occasion_move(board,player,actions) != False:
                    return make_occasion_move(board,player,actions)
                    
                import random
                print('\n\nrandom play\n\n')
                return random.choice(actions)
            else:
                import random
                print('\n\nrandom play\n\n')
                return random.choice(actions)
        elif actions[0].get_action_as_dict()['action_type'] == MorabarabaActionType.ADD:
            
            # board = state.get_board()
            # scores = dict(zip(actions,[score_move(board,4,player,action.get_action_as_dict()['action']['to']) for action in actions]))
            # print("\n\n\n",scores.values(),"\n\n\n")
            # max_actions = [act for act in scores.keys() if scores[act] == max(scores.values())]
            # import random
            # return random.choice(max_actions)
            action = make_occasion_add(board,player,actions)
            if action != False:
                return action
            import random
            for action in actions:
                if action.get_action_as_dict()['action']['to'] in [(1,5),(5,1),(1,1),(5,5)]:
                    print("\n\naction\n\n")
                    return action
            
        elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.STEAL: 
            action_choice=STEAL(board,player,actions)
            if action_choice != False :
                return action_choice
            import random 
            print('\n\nrandom play\n\n')
            return random.choice(actions)
        elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.FLY: 
            if fly(board,player,actions) != False:
                return fly(board,player,actions)
            import random 
            print('\n\nrandom play\n\n')
            return random.choice(actions)
        import random 
        print('\n\nrandom play\n\n')
        return random.choice(actions)
    # except:
    #     actions = MorabarabaRules(player).get_player_actions(state,player)
    #     import random
    #     print("\nexeption\n")
    #     return random.choice(actions)
            
class AI(MorabarabaPlayer):
    name = "intellegent"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        
        return play(state, self.position)
