from math import exp
from core import Color
import random
from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_action import MorabarabaAction
from morabaraba.morabaraba_action import MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from morabaraba.morabaraba_board import MorabarabaBoard

#code a verifier

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
    for action in actions:
        if is_making_mill(board,-1*player, action.get_action_as_dict()['action']['to'])[0]:
            return action
    return False


def ADD(board,player,actions) :
    k=-1
    for cell in board.get_all_empty_cells() :
        k+=1
        if is_making_mill(board,player,cell)[0]==True:
            print("\n\n\n\nadd\n\n\n\n")
            return actions[k] 
    return False

def STEAL(board,player,actions) :
    for cell in board.get_all_empty_cells() :
        mills=is_making_mill(board,player,cell) 
        if mills[0]==True :
            for mill_cell in mills[1][0] :
                if mill_cell != cell :
                    for action in actions :
                        if action.get_action_as_dict()['action']['at'] == mill_cell :
                            print("\n\n\n\nsteal \n\n\n\n")
                            return action
                        
    if actions[0].get_action_as_dict()['action_type'] == MorabarabaActionType.MOVE :
        for action in actions:
            for piece in board.get_player_pieces_on_board(Color(player)):
                if is_making_mill(board,player, action.get_action_as_dict()['action']['at'])[0]:
                    for move in get_effective_cell_moves(bord,piece):
                        if action.get_action_as_dict()['action']['at'] == move:
                            print("\n\nmy own steal \n")
                            return action
                elif is_making_mill(board,player, action.get_action_as_dict()['action']['at'])[0]:
                    print("\n\nmy own steal the second else \n")
                    return action
     
    return False 



def make_occasion_add(board,player, actions):
    possible_occasion = []
    occasion = []
    good_occasion = []
    good = []
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    for mill in board.mills():
            for piece in pieces:
                for adv_piece in adv_pieces:
                    if piece in mill and adv_piece not in mill:
                        good_occasion.append(mill)
    if good_occasion:
        for good_occ in good_occasion:
            for occ in good_occ:
                if occ in board.get_all_empty_cells():
                    good.append(occ)
    if good:
        occurences = [good.count(i) for i in set(good)]
        for action in actions:
            if action.get_action_as_dict()['action']=={'to': good[occurences.index(max(occurences))]}:
                print("\n\ngood occasions \n",max(occurences),"\n")
                print(set(good))
                print(occurences)
                return action

    # pour bloquer les eventuelles mills overts de l'adversaire

    pieces = board.get_player_pieces_on_board(Color(-1*player))
    adv_pieces = board.get_player_pieces_on_board(Color(player))

    for mill in board.mills():
            for piece in pieces:
                for adv_piece in adv_pieces:
                    if piece in mill and adv_piece not in mill:
                        good_occasion.append(mill)
    if good_occasion:
        for good_occ in good_occasion:
            for occ in good_occ:
                if occ in board.get_all_empty_cells():
                    good.append(occ)
    if good:
        occurences = [good.count(i) for i in good]
        for action in actions:
            if action.get_action_as_dict()['action']=={'to': good[occurences.index(max(occurences))]}:
                print("\n\ngood occasions \n\n")
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
    
#--------------------------------------------****--------------------

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
                            print("\n\npriorite move \n\n")
                            return action
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
        
        mills = player_mill(board,player)
        if mills:
            for mill in mills:
                for action in actions:
                    if action.get_action_as_dict()['action']['at'] == mill:
                        return action
        pieces = board.get_player_pieces_on_board(Color(player))
        cells = []
        movable_pieces = []
        movables = [get_effective_cell_moves(board,piece) for piece in pieces]
        for movable in movables:
            for movable_piece in movable:
                if movable_piece in cells:
                    movable_pieces.append(movable_piece)
                cells.append(movable_piece)
        if movable_pieces : 
            for action in actions:
                if action.get_action_as_dict()['action']['at'] == movable_pieces[0]:
                    print("\n\nsecondaire \n\n")
                    return action
        return False

def choix(state, player, action):
    board = state.get_board()
    possibles_moves = get_effective_cell_moves(board,action.get_action_as_dict()['action']['at'])
    for move in possibles_moves:
        board.empty_cell(action.get_action_as_dict()['action']['at'])
        board.fill_cell(move, Color(player))
        state.set_board(board)
        actions = MorabarabaRules(player).get_player_actions(state,player)
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill :
                            for adv_action in MorabarabaRules(-1*player).get_player_actions(state,-1*player):
                                if adv_action.get_action_as_dict()['action']['to'] != cell:
                                    print('\n\n ca fait de mill en avant\n\n')
                                    return True   
                            print('\n\n ca pourait causer de mill en avant\n\n')
                            return 1
    return False
        
def Check_block(actions,board,player):
    for action in actions:
        if is_making_mill(board,-1*player,action.get_action_as_dict()['action']['at'])[0]:
            if len(actions) > 1:
                print('\n\nRemove Done\n\n')
                actions.remove(action)
    return actions
    
def play(state, player):

    actions = MorabarabaRules(player).get_player_actions(state,player)
    board = state.get_board()

    if len(actions)==0:
        return None
    else:
        if actions[0].get_action_as_dict()['action_type'] == MorabarabaActionType.MOVE:
            action_choice=Check_Move(state,board,player,actions)
            if action_choice != False :
                 return action_choice
            action_choice=Check_Move(state,board,-1*player,actions)
            if action_choice != False :
                return action_choice
            
            elif action_choice == False:
                for action in actions:
                    if choix(state, player, action)== True:
                        return action
                for action in actions:
                    if choix(state, player, action)== 1:
                        return action
                actions = Check_block(actions, state.get_board(),player)
                import random
                print('\n\nrandom play\n\n')
                return random.choice(actions)
            else:
                import random
                print('\n\nrandom play\n\n')
                return random.choice(actions)
        elif actions[0].get_action_as_dict()['action_type'] == MorabarabaActionType.ADD:
            action_choice=ADD(board,player,actions)
            if action_choice != False :
                 return action_choice
            action_choice=ADD(board,-1*player,actions)
            if action_choice != False :
                return action_choice
            action = make_occasion_add(board,player,actions)
            if action != False:
                return action
        elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.STEAL: 
            action_choice=STEAL(board,player*-1,actions)
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
            

class AI(MorabarabaPlayer):
    name = "strong"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        
        return play(state, self.position)

