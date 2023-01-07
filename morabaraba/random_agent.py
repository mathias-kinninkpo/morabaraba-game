from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_action import MorabarabaAction
from morabaraba.morabaraba_action import MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from core import Color
import random


class AI(MorabarabaPlayer):
    name = "SGCM strong"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time): 
        # try:
            rules=MorabarabaRules(self.position)
            board=state.get_board()
            actions=rules.get_player_actions(state,self.position)
            if actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.ADD :
                # cell = Make_occasion_add(state,self.position)
                # for action in actions:
                #     if action.get_action_as_dict()['action']['to'] == cell:
                #         return action
                action_choice=ADD(state,self.position,actions)
                if action_choice != False :
                    return action_choice
                action_choice=more_occasion(state,-1*self.position,actions)
                if action_choice != False :
                    return action_choice
                action_choice=ADD_block(state,-1*self.position,actions)
                if action_choice != False :
                    return action_choice
                return Make_occasion(rules,state,self.position,actions)
            elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.STEAL  : 
                action_choice=STEAL(rules,state,-1*self.position,actions)
                print(action_choice)
                if action_choice != False :
                    return action_choice
                return MorabarabaRules.random_play(state, self.position)
            elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.MOVE:
                action_choice=Move(state,rules,actions,self.position,self.position)
                if action_choice != False :
                    return action_choice
                action_choice=Move(state,rules,actions,-1*self.position,self.position)
                if action_choice != False :
                    return action_choice
                return Make_occasion(rules,state,self.position,actions)
            else :
                action_choice=Move(state,rules,actions,self.position,self.position)
                if action_choice != False :
                    return action_choice
                action_choice=Move(state,rules,actions,-1*self.position,self.position)
                if action_choice != False :
                    return action_choice
                return Make_occasion(rules,state,self.position,actions)
        # except:
        #     rules=MorabarabaRules(self.position)
        #     actions=rules.get_player_actions(state,self.position)
        #     return random.choice(actions)




def ADD_block(state,player,actions) :
    board=state.get_board()
    cells=[]
    for cell in board.get_all_empty_cells() :
        if is_making_mill(board,player,cell)[0] == True :
            cells.append(cell)

    if len(cells) == 0 :
         return False
    else :
        choices=ADD_and_Ocassion(state,player)
        choice=[cell for cell in cells if cell in choices]
        if len(choice) == 0 :
            choice=cells[0]
        else :
            choice=choice[0]
        for action in actions :
            if action.get_action_as_dict()["action"]["to"] == choice :
                return action

def get_piece_mills(state,player,number):
    board = state.get_board()
    pieces = board.get_player_pieces_on_board(Color(player))
    adv_pieces = board.get_player_pieces_on_board(Color(-1*player))
    cells_mill = []
    cells_pieces = []
    for mill in board.mills():
        if all([adv_piece not in mill for adv_piece in adv_pieces]) and len(set(mill) & set(pieces)) == number:
            for cell in mill:
                if cell in board.get_all_empty_cells():
                    cells_mill.append(cell)
                else:
                    cells_pieces.append(cell)
    return [cells_mill,cells_pieces]

def save_mills(state,player):
    board = state.get_board()
    cells = get_piece_mills(state,player,2)[0]
    pieces = get_piece_mills(state,player,2)[1]
    for cell in cells:
        for move in MorabarabaRules.get_rules_possibles_moves(cell,board):
            if move in board.get_player_pieces_on_board(Color(player)):
                pieces.append(move)
                return [True,pieces]
    return [False,[]]

def block_mills(state,player):
    board = state.get_board()
    adv_cells = get_piece_mills(state,-1*player,2)[0]
    pieces = board.get_player_pieces_on_board(Color(player))
    for adv_cell in adv_cells:
        for piece in pieces :
            cells=rules.get_effective_cell_moves(state,piece)

            if len(cells) != 0 :
                for cell in cells :
                    board.empty_cell(piece)
                    board.fill_cell(cell,Color(player))
                    new_pieces=board.get_player_pieces_on_board(Color(player))
                    for new_piece in new_pieces:
                        if any([adv_cell == move for move in MorabarabaRules.get_rules_possibles_moves(new_piece)]):
                            return [True,piece,cell]
                    board.empty_cell(cell)
                    board.fill_cell(piece,Color(player))
    return [False,None,None]

def regroupe(state,player,actions):
    board = state.get_board()
    for piece in get_piece_mills(state,player,1)[0]:
        for action in actions:
            if action.get_action_as_dict()['action']['to'] == piece:
                print("\n\nRAPROCHEMENT DES PIECES\n\n")
                return [True,action]
    return [False, None]
 

            
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

        if len(player_mills) == 0: 
            is_player_mill = False 
        else : is_player_mill = True 
    return [ is_player_mill , player_mills ]

def is_effective_making_mill(state,player,rules,cell,mill) :
    actions=rules.get_player_actions(state,player)
    is_mill=False
    for action in actions :
        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill and is_mill == False:
            is_mill=True
    return is_mill

def can_make_mill(state,rules,player) :
    for cell in state.get_board().get_all_empty_cells() :
        mills=is_making_mill(state.get_board(),player,cell)
        if  mills[0] == True:
            for mill in mills[1] :
                if is_effective_making_mill(state,player,rules,cell,mill) == True :
                    return True
    return False
def ADD(state,player,actions) :
    board=state.get_board()
    cells=[]
    for cell in board.get_all_empty_cells() :
        if is_making_mill(board,player,cell)[0] == True :
            for action in actions:
                if action.get_action_as_dict()['action']['to'] == cell:
                    return action
    return False
            # cells.append(cell)
    # return cells


def create_double_occasions(state,player):
    board = state.get_board()
    table_cell = []
    for cell in board.get_all_empty_cells():
        board.fill_cell(cell,Color(player))
        state.set_board(board)
        my_potential_occasion,my_occasions=Occasion(state,player)
        if my_potential_occasion[0] > 1 :
            table_cell.append(cell)
        board.empty_cell(cell)
        state.set_board(board)
    if table_cell:
        return [True,table_cell]
    return[False,[]]
def check_double(state,player,pieces):
    board = state.get_board()
    for piece in pieces:
        board.fill_cell(piece,Color(player))
        state.set_board(board)
        double_occasions, one_occasions = Occasion(state,-1*player)
        if double_occasions[0] == 0:
            return [True,piece]
        board.empty_cell(piece)
        state.set_board(board)
    return [False,[]]

def check_block(state,player,piece):
    board = state.get_board()
    board.fill_cell(piece,Color(player))
    if ADD(state,-1*player):
        return True
    False


def Make_occasion_add(state,player):
    wins = ADD(state,player)
    double_occasions, one_occasions = Occasion(state,player)
    adv_double_occ, adv_one_occ = Occasion(state,-1*player)
    if wins:
        if double_occasions[0] > 0:
            for occ in double_occasions[1]:
                if check_block(state,player,occ) == False:
                    return occ
            return random.choice(double_occasions[1])
        for win in wins:
            if win in one_occasions:
                return win
        for win in wins:
            if win in adv_one_occ or win in adv_one_occ:
                return win
        return random.choice(wins)
    blocks = ADD(state,-1*player)
    occasion_in_advance = create_double_occasions(state,player)
    occurences = [occasion_in_advance[1].count(i) for i in occasion_in_advance[1]]
    if player == -1 and state.in_hand[player] == 11:
        if occurences:
            print(occurences)
            print('\n\n',occasion_in_advance[1][occurences.index(max(occurences))],' DOUBLE OCCASION IN ADVANCE \n\n')
            return occasion_in_advance[1][occurences.index(max(occurences))]
    if blocks:
        if occasion_in_advance[0] == True:
            for block in blocks:
                if block in occasion_in_advance[1]:
                    return block
        if double_occasions[0] > 0 and len(blocks) == 1:
            return random.choice(double_occasions[1])
        for block in blocks:
            if block in one_occasions:
                return block
        for block in blocks:
            if block in adv_one_occ:
                return block
        return random.choice(blocks)
    if double_occasions[0] > 1:
        for occ in double_occasions[1]:
            if check_block(state,player,occ) == False:
                return occ
        return random.choice(double_occasions[1])
    if adv_double_occ[0] > 1:
        if check_double(state,player,one_occasions)[0]:
            return check_double(state,player,one_occasions)[1]
        for occ in adv_double_occ:
            if occ in one_occasions:
                return occ
        return random.choice(adv_double_occ[1])
    for occ in one_occasions:
        if occ in occasion_in_advance and check_block(state,player,occ) == False:
            return occ
        if occ in occasion_in_advance:
            return occ
    intersection = set(one_occasions) & set(adv_one_occ)
    if len(intersection) > 0:
        for occ in intersection:
            if check_block(state,player,occ) == False:
                return occ
        return random.choice([i for i in intersection])
    only_in_mill = get_piece_mills(state,-1*player,1)[0]
    if only_in_mill:
        for cell in only_in_mill:
            if cell in occasion_in_advance:
                return cell
    if one_occasions:
        for occ in one_occasions:
            if check_block(state,player,occ) == False:
                return occ
        return random.choice(one_occasions)
    if adv_one_occ:
        return random.choice(adv_one_occ)
    cells = state.get_board().get_all_empty_cells()
    if (5,1) in cells:
        return (5,1)
    print("\n\nrandom play\n\n")
    return random.choice(cells)
        



def ADD_and_Ocassion(state,player) :
    my_potential_occasion,my_occasions=Occasion(state,player)
    adverse_potential_occasion,adverse_occasions=Occasion(state,-1*player)
    if (len(my_occasions) == 0 and len(adverse_occasions) == 0 ) :
            choice=[(5,1),(1,5)]
    elif len(my_occasions) == 0 and len(adverse_occasions) != 0 :
        choice=[(1,5)]
    elif len(my_occasions) != 0 and len(adverse_occasions) == 0 :
        choice=[my_potential_occasion[1]]
    else :
        if my_potential_occasion[0] >= adverse_potential_occasion[0] and my_potential_occasion[0] != 1 :
            choice=[my_potential_occasion[1]]
        elif adverse_potential_occasion[1] in my_occasions and adverse_potential_occasion[0] !=1 :
            choice=[adverse_potential_occasion[1]]
        elif adverse_potential_occasion[0] > my_potential_occasion[0] :
            choice=[adverse_potential_occasion[1]]
        else :
            choice=[cell for cell in my_occasions if cell in adverse_occasions]
            if len(choice) == 0 :
                if player == -1 :
                    choice=[list(reversed(my_occasions[0]))]
                else :
                    
                    choice=[list(reversed(adverse_occasions[0]))]
                
    return choice
    
    

def STEAL(rules,state,player,actions) :
    board=state.get_board()
    if state.get_latest_move()['action_type'] ==  "ADD" :
        choice=""
        in_between_more_my_piece,in_between_my_piece,in_double_occasion=In_between_my_piece(board,player)
        potential_fatal_cell,fatal_cells=Fatal_cells(board,player)
        adverse_potential_occasion,adverse_occasions=Occasion(state,player)
        if len(in_between_my_piece) == 0 and len(fatal_cells) == 0 and len(adverse_occasions) !=0 :
            choice=Cell(board,player,adverse_potential_occasion[1])
        elif len(in_between_my_piece) == 0 and len(fatal_cells) !=0 :
            choice=potential_fatal_cell[1]
        elif len(in_between_my_piece) !=0 and len(fatal_cells) == 0 :
            if len(adverse_occasions) == 0 and in_double_occasion[0] == True:
                choice=in_double_occasion[1][0]
            else :
                choice=in_between_more_my_piece[1]
        elif len(in_between_my_piece) !=0 and len(fatal_cells) !=0 and potential_fatal_cell[1] in in_between_my_piece :
            choice=potential_fatal_cell[1]
        elif len(in_between_my_piece) !=0 and len(fatal_cells) !=0 and potential_fatal_cell[1] not in in_between_my_piece :
            intersection=[x for x in in_between_my_piece if x in fatal_cells]
            if len(intersection) !=0 :
                choice=intersection[0]
            else :
                choice=in_between_more_my_piece[1]
        else :
            choice=(6,0)
        for action in actions :
            if action.get_action_as_dict()['action']['at'] == choice :
                return action

    else :
        piece=Steal_cell(rules,state,player)
        if piece != False :
            for action in actions :
                if action.get_action_as_dict()['action']['at'] == piece :
                    return action
        else :
            player_mills=board.player_mills(-1*player)
            if len(player_mills) != 0 :
                for player_mill in player_mills :
                    for mill_cell in player_mill :
                        cells=get_effective_cell_moves(state,mill_cell,player)
                        for cell in cells :
                            if cell in board.get_player_pieces_on_board(Color(player)) and free(state,rules,cell,player) == True:
                                for action in actions :
                                    if action.get_action_as_dict()['action']['at'] == cell :
                                            return action
            else :
                for cell in board.get_all_empty_cells() :
                    mills=is_making_mill(board,player,cell) 
                    if mills[0]==True :
                        for mill_cell in mills[1][0] :
                            if mill_cell != cell :
                                for action in actions :
                                    if action.get_action_as_dict()['action']['at'] == mill_cell :
                                        return action
    return actions[0]

def free(state,rules,cell,player) :
    board=state.get_board()
    pieces=board.get_player_pieces_on_board(Color(player))
    board.empty_cell(cell)
    state.set_board(board)
    for piece in pieces :
        cells=rules.get_effective_cell_moves(state,piece)
        if cell in cells :
            mill=[mill for mill in board.mills() if piece in mill and mill in board.player_mills(player)]
            if len(mill) == 0 :
                return True
            else :
                return False
    return True

def Steal_cell(rules,state,player) :
    board=state.get_board()
    all_pieces=board.get_player_pieces_on_board(Color(player))
    player_mills=board.player_mills(player)
    pieces_mills=[]
    mills=[]
    cells_mill=[]
    is_mill=False

    for mill in player_mills :
        for mill_cell in mill :
           pieces_mills.append(mill_cell)  

    pieces=[x for x in all_pieces if x not in pieces_mills]

    for piece in all_pieces :
        cells=rules.get_effective_cell_moves(state,piece)
        for cell in cells :
            mills=is_making_mill(board,player,cell)
            if mills[0] == True and (len([mill for mill in mills[1] if piece in mill and cell in mill]) == 0 or len(mills[1])>=2) and is_mill==False:
                is_mill=True

    if is_mill == True :

        for piece in pieces :
            is_mill=False
            board.empty_cell(piece)
            for x in [y for y in pieces if y != piece] :
                if is_mill == False :
                    cells=get_effective_cell_moves(state,x,player)
                    for cell in cells :
                        mills=is_making_mill(board,player,cell)
                        if mills[0] == True and (len([mill for mill in mills[1] if x in mill and cell in mill]) == 0 or len(mills[1])>=2) and is_mill == False:
                            is_mill=True
            if is_mill == False :
                print(piece)
                return piece
            board.fill_cell(piece,Color(player))
        
        for piece in pieces_mills :
            cells=rules.get_effective_cell_moves(state,piece)
            for cell in cells :
                mills=is_making_mill(board,player,cell)
                if mills[0] == True and (len([x for x in mills[1] if piece in x and cell in x]) == 0 or len(mills[1])>=2) :
                    for mill in mills[1] :
                        for mill_cell in mill :
                            if mill_cell != cell :
                                return mill_cell

        for piece in pieces :
            cells=rules.get_effective_cell_moves(state,piece)
            for cell in cells :
                mills=is_making_mill(board,player,cell)
                if mills[0] == True and len(mills[1])>=2 and (len([mill for mill in mills[1] if piece in mill and cell in mill]) == 0 or len(mills[1])>=2):
                    return piece

        for piece in pieces :
            cells=rules.get_effective_cell_moves(state,piece)
            for cell in cells :
                mills=is_making_mill(board,player,cell)
                if mills[0] == True and (len([mill for mill in mills[1] if piece in mill and cell in mill]) == 0 or len(mills[1])>=2) :
                    return piece
    else :
        my_pieces=board.get_player_pieces_on_board(Color(player*-1))
        board_mills=board.mills()
        for piece in pieces :
            new_pieces=[]
            mils=[mill for mill in board_mills if piece in mill]
            for mill in mils :
                for mill_cell in mill :
                    if mill_cell in my_pieces :
                        new_pieces.append(mill_cell)

            board.empty_cell(piece)
            for my_piece in new_pieces :
                cells=rules.get_effective_cell_moves(state,my_piece)
                for cell in cells :
                    mills=is_making_mill(board,player*-1,cell)
                    if mills[0] == True and (len([mill for mill in mills[1] if my_piece in mill and cell in mill]) == 0 or len(mills[1])>=2) :
                        return piece

            board.fill_cell(piece,Color(player))
    
    return False

     
def Move(state,rules,actions,player_current,player) :
    action_wins = []
    board=state.get_board()
    if player == player_current :
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player_current,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill:
                            action_wins.append(action)
        if len(action_wins) > 1:
            for action in action_wins:
                mills = is_making_mill(board,-1*player,action.get_action_as_dict()["action"]["at"])
                if mills[0]:
                    for mill in mills[1]:
                        if ((is_effective_making_mill(state,-1*player,rules,action.get_action_as_dict()['action']['at'],mill) ==  True ) or (ordinateur(state,rules,[],-1*player,action.get_action_as_dict()['action']['at'])[0] and ordinateur(state,rules,[],-1*player,action.get_action_as_dict()['action']['at'])[2] == action.get_action_as_dict()['action']['at'])) and len(action_wins) >1: 
                            action_wins.remove(action)
                            print('\nwin danger\n')
                        elif len(action_wins) >1 and action.get_action_as_dict()['action']['at'] in get_adv_possible_destination(board,-1*player):
                            action_wins.remove(action)
                            print('\nwin danger\n')
            return random.choice(action_wins)
        elif len(action_wins) == 1:
            return random.choice(action_wins)
                         
    else :
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player_current,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill  and is_effective_making_mill(state,player_current,rules,cell,mill) == True :
                            action_wins.append(action)
                        

        if len(action_wins) >= 1:
            return random.choice(action_wins)
    return False

def Cell(board,player,cell) :
    is_cell=True
    mills=[mill for mill in board.mills() if cell in mill]
    for mill in mills :
        for mill_cell in mill :
            if mill_cell in board.get_player_pieces_on_board(Color(player)):
                cell=mill_cell
            if mill_cell in board.get_player_pieces_on_board(Color(-1*player)) :
                is_cell=False
        if is_cell == True :
            return cell

def Fatal_cells(board,player) :
    fatal_cells=[]
    potential_fatal_cell=[0,(0,0)]
    for cell in board.get_all_empty_cells() :
        mills=is_making_mill(board,player,cell)
        if mills[0] == True :
            for mill in mills[1] :
                for mill_cell in mill :
                    if mill_cell != cell :
                        fatal_cells.append(mill_cell)
    for fatal_cell in fatal_cells :
        if fatal_cells.count(fatal_cell) > potential_fatal_cell[0] :
            potential_fatal_cell=[fatal_cells.count(fatal_cell),fatal_cell]
    return potential_fatal_cell,fatal_cells

def In_between_my_piece(board,player) :
    mills=board.mills()
    in_between_my_piece=[]
    in_double_occasion=[False,[]]
    in_between_more_my_piece=[0,(0,0)]
    pieces = board.get_player_pieces_on_board(Color(-1*player))
    pieces_adverses = board.get_player_pieces_on_board(Color(player))
    for mill in mills :
        empty_cell=0
        my_color=[]
        not_my_color=[]
        for mill_cell in mill :
            if mill_cell in pieces :
                my_color.append(mill_cell)
            elif mill_cell in pieces_adverses :
                not_my_color.append(mill_cell)
            else :
                empty_cell+=1
        if empty_cell == 0 and len(my_color) == 2 :
            in_between_my_piece.append(not_my_color[0])
        if empty_cell == 1 and len(my_color) == 1 :
            if not_my_color[0] in in_double_occasion[1] :
                in_double_occasion[0]=True
            in_double_occasion[1].append(not_my_color[0])

    for cell in in_between_my_piece :
        if in_between_my_piece.count(cell) > in_between_more_my_piece[0] :
            in_between_more_my_piece=[in_between_my_piece.count(cell),cell]
  
    return in_between_more_my_piece,in_between_my_piece,in_double_occasion
            

def more_occasion(state,player,actions) :
    adverse_potential_occasion,adverse_occasions=Occasion(state,player)
    my_potential_occasion,my_occasions=Occasion(state,-1*player)
    if adverse_potential_occasion[0] > 2 and my_potential_occasion[0] < 2 :
        for action in actions :
            if action.get_action_as_dict()['action']['to'] == adverse_potential_occasion[1]  :
                    return action
    return False


def Occasion(state,player) :
    board=state.get_board()
    occasions=[]
    mills = board.mills()
    pieces = board.get_player_pieces_on_board(Color(player))
    pieces_adverses = board.get_player_pieces_on_board(Color(-1*player))
    if len(pieces) == 0 :
        return [0,[]] , []
    else :
        for piece in pieces :
            for mill in mills :
                luck=True
                if piece in mill :
                    for mill_cell in mill :
                        if mill_cell in pieces_adverses :
                            luck=False
                    if luck == True :
                        for mill_cell in mill :
                            if mill_cell != piece and mill_cell in board.get_all_empty_cells() :
                                occasions.append(mill_cell)
        luck=[0,[]]
        for occasion in occasions :
            Count=occasions.count(occasion)
            if Count > 1 and occasion not in luck[1]:
                if Count > luck[0] :
                    luck[1].insert(0,occasion)
                    luck[0]=Count
                else :
                    luck[1].append(occasion)
        occasions=[cell for cell in occasions if cell not in luck[1]]
        return luck,occasions

def Make_occasion(rules,state,player,actions) :
    board=state.get_board()
    if actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.ADD :

        choice=ADD_and_Ocassion(state,player)
        
        for cell in choice :
            for action in actions :
                if action.get_action_as_dict()['action']['to'] == cell  :
                        return action
        print("\n\n randommmmm",choice)
        return MorabarabaRules.random_play(state,player)
               
    elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.MOVE :

        dont_move_cell=[]
        if can_make_mill(state,rules,player*-1) == False :
            piece_saved = save_mills(state,player)
            if piece_saved[0]:
                print("\n\nsaved",piece_saved)
                for cell in piece_saved[1]:
                    for action in actions:
                        if action.get_action_as_dict()['action']['at'] == cell and len(actions) >1:
                            actions.remove(action)
                            print('\n\nPIECES SAVED REMOVED FROM ACTIONS\n\n')
            pieces=get_pieces_can_move(state,rules,actions,player)
            movable  = ordinateur(state,rules,pieces,-1*player)
            if movable[0]:
                for action in actions:
                    if action.get_action_as_dict()['action']['at'] == movable[1] and action.get_action_as_dict()['action']['to'] == movable[2]:
                        print('\n\nWILL WIN\n\n')
                        return action
            occ = regroupe(state,player,actions)
            if occ[0]:
                return occ[1]
            pieces=get_pieces_can_move(state,rules,actions,player)
            movable  = ordinateur(state,rules,pieces,player)
            if movable[0]:
                for action in actions:
                    if action.get_action_as_dict()['action']['at'] == movable[1] and action.get_action_as_dict()['action']['to'] == movable[2]:
                        print('\n\nWILL WIN\n\n')
                        return action
            choice=contracte(dont_move_cell,actions,state,rules,player)
            
            
            if choice != False :
                return choice
            
            return actions[0]
        
        for mill in board.player_mills(player) :
            for mill_cell in mill :
                dont_move_cell.append(mill_cell)
        
        choice=contracte(dont_move_cell,actions,state,rules,player)
        if choice != False :
            return choice

        return actions[0]
    return actions[0]

def ordinateur(state,rules,pieces,player,cell = (0,0)) :
    board=state.get_board()
    if len(pieces) == 0 :
        pieces=board.get_player_pieces_on_board(Color(player))
    if cell != (0,0):
        board.empty_cell(cell)
    for piece in pieces :
        cells=rules.get_effective_cell_moves(state,piece)
        if len(cells) != 0 :
            for cell in cells :
                board.empty_cell(piece)
                board.fill_cell(cell,Color(player))
                new_pieces=board.get_player_pieces_on_board(Color(player))
                for new_piece in new_pieces :
                    cells_move=get_effective_cell_moves(state,new_piece,player)
                    for cell_move in cells_move :
                        mills=is_making_mill(board,player,cell_move)
                        if mills[0] == True  and all([move not in  board.get_player_pieces_on_board(Color(-1*player)) for move in rules.get_rules_possibles_moves(cell_move,board)]) :
                            print(piece,cell)
                            return [True,piece,cell]
                board.empty_cell(cell)
                board.fill_cell(piece,Color(player))
    return [False,False,False]

def get_effective_cell_moves(state, cell,player = 0) :
    board = state.get_board()
    if board.is_cell_on_board(cell):
        possibles_moves = MorabarabaRules.get_rules_possibles_moves(cell, board)
        effective_moves = []
        forbidden_cell = []
        if player == -1:                 
            forbidden_cell = state.player1_forbidden_cell
        elif player == 1: 
            forbidden_cell = state.player2_forbidden_cell
        if forbidden_cell[1] != None and forbidden_cell[1] in possibles_moves:
            possibles_moves.remove(forbidden_cell[1])
            print(forbidden_cell)
        for move in possibles_moves:
            if board.is_empty_cell(move):
                effective_moves.append(move)
        return effective_moves 

def get_pieces_can_move(state,rules,actions,player) :
    pieces=[]
    rest_actions=which_move(state,rules,actions,player)
    for action in rest_actions :
        pieces.append(action.get_action_as_dict()["action"]["at"])
    return pieces

def contracte(dont_move_cell,actions,state,rules,player) :

    new_actions=[new_action for new_action in actions if new_action.get_action_as_dict()["action"]['at'] not in dont_move_cell]
    dont_do_action=[action for action in actions if action.get_action_as_dict()["action"]["at"] in dont_move_cell]
    rest_actions=which_move(state,rules,new_actions,player)
    if len(rest_actions) != 0  :
        choice=regroup_pieces(state.get_board(),player,rest_actions)
        print(choice)
        if choice == False :
            choice=random_play(rest_actions)
            print("\nrandom play\n")
    elif len(dont_do_action) != 0 :
        choice=regroup_pieces(state.get_board(),player,dont_do_action)
        if choice == False :
            print("\nrandom play\n")
            choice=random_play(dont_do_action)
    else:
        choice=random_play(new_actions)
        print("\nrandom play\n")
         
    return choice
        
def regroup_pieces(board,player,actions) :
    posible_destination = [i for i in set(get_adv_possible_destination(board,player)) & set(board.get_all_empty_cells())]
    possible_occasion = get_occasions(board,player)
    for action in actions:
        if action.get_action_as_dict()['action']['to'] in set(posible_destination) & set(possible_occasion[2]):
            print("\n\nregroupement\n\n")
            return action
    return False

def get_adv_possible_destination(board, player, mill = []):
    adv_possible_destination = []
    for piece in set(board.get_player_pieces_on_board(Color(player))) - set(mill):
        for move in MorabarabaRules.get_rules_possibles_moves(piece,board):
            adv_possible_destination.append(move)
    return adv_possible_destination

def get_occasions(board,player):
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

def which_move(state,rules,actions,player) :
    board=state.get_board()
    rest_actions=[]
    danger_acttions = []
    for action in actions :
        tmp=action.get_action_as_dict()
        at = tmp['action']['at']
        to = tmp['action']['to']
        board.empty_cell(at)
        board.fill_cell(to,Color(player))
        state.set_board(board)
        mills=is_making_mill(board,player*-1,at)
        if mills[0] == True and any([at == move for move in set(get_adv_possible_destination(board,-1*player)) & set(board.get_all_empty_cells())]):
            danger_acttions.append(action)
        rest_actions.append(action)
        board.empty_cell(to)
        board.fill_cell(at,Color(player))
    if danger_acttions:
        for danger_acttion in danger_acttions:
            if danger_acttion in rest_actions and len(rest_actions) > 1:
                rest_actions.remove(danger_acttion)
                print("remove done danger")
    return rest_actions   

def random_play(actions) :
    if len(actions) != 0 :
        print("\n\n random play")
        return random.choice(actions)
    return False