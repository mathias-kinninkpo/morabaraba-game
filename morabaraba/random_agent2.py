from morabaraba.morabaraba_player import MorabarabaPlayer
from morabaraba.morabaraba_action import MorabarabaAction
from morabaraba.morabaraba_action import MorabarabaActionType
from morabaraba.morabaraba_rules import MorabarabaRules
from core import Color
import random


def more_occasion(state,player,actions) :
    adverse_potential_occasion,adverse_occasions=Occasion(state,player)
    my_potential_occasion,my_occasions=Occasion(state,player)
    if adverse_potential_occasion[0] > 2 and my_potential_occasion[0] < 2 :
        for action in actions :
            if action.get_action_as_dict()['action']['to'] == adverse_potential_occasion[1]  :
                    return action
    return False

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

def is_effective_making_mill(state,player,rules,cell,mill) :
    actions=rules.get_player_actions(state,player)
    is_mill=False
    for action in actions :
        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill and is_mill == False:
            is_mill=True
    return is_mill

def ADD(state,player,actions) :
    board=state.get_board()
    cells=[]
    for cell in board.get_all_empty_cells() :
        if is_making_mill(board,player,cell)[0] == True :
            cells.append(cell)

    if len(cells) == 0 :
        return False
    else :
        my_potential_occasion,my_occasions=Occasion(state,player)
        choice=[cell for cell in cells if cell == my_potential_occasion[1] ]
        if len(choice) == 0 :
            choice=cells[0]
        else :
            choice=choice[0]
        for action in actions :
            if action.get_action_as_dict()["action"]["to"] == choice :
                return action

def can_make_mill(state,rules,player) :
    for cell in state.get_board().get_all_empty_cells() :
        mills=is_making_mill(state.get_board(),player,cell)
        if  mills[0] == True:
            for mill in mills[1] :
                if is_effective_making_mill(state,player,rules,cell,mill) == True :
                    return True
    return False


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
                        mills=[mill for mill in board.mills() if mill_cell in mill and mill not in player_mills] 
                        for mill in mills :
                            for cell in mill :
                                if cell in board.get_player_pieces_on_board(Color(player)) :
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
    return False 

def Steal_cell(rules,state,player) :
    board=state.get_board()
    pieces=board.get_player_pieces_on_board(Color(player))
    player_mills=board.player_mills(player)
    pieces_mills=[]
    for mill in player_mills :
        for mill_cell in mill :
           pieces_mills.append(mill_cell)  

    pieces=[x for x in pieces if x not in pieces_mills]

    for piece in pieces :
        is_mill=False
        old_board=state.get_board()
        board=old_board
        board.empty_cell(piece)
        state.set_board(board)
        for x in [y for y in pieces if y != piece] :
            cells=rules.get_effective_cell_moves(state,x)
            for cell in cells :
                mills=is_making_mill(board,player,cell)
                if mills[0] == True and len([mill for mill in mills[1] if x in mill and cell in mill]) != 0 :
                    is_mill=True
        if is_mill == False :
            return piece
        else :
            state.set_board(old_board)
    return False

     
def Move(state,rules,actions,player_current,player) :
   board=state.get_board()
   if player == player_current :
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player_current,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill:
                            return action
   else :
        for cell in board.get_all_empty_cells() :
            mills=is_making_mill(board,player_current,cell) 
            if mills[0]==True :
                for mill in mills[1] :
                    for action in actions :
                        if action.get_action_as_dict()['action']['to'] == cell and action.get_action_as_dict()['action']['at'] not in mill  and is_effective_making_mill(state,player_current,rules,cell,mill) == True :
                            return action
   return False

def Cell(board,player,cell) :
    is_cell=True
    mills=[mill for mill in board.mills() if cell in mill]
    for mill in mills :
        for mill_cell in mill :
            if mill_cell in board.get_player_pieces_on_board(Color(player)) :
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
            


def Occasion(state,player) :
    occasions=[]
    board=state.get_board()
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
        luck=[0,(0,0)]
        if len(occasions) == 0 :
            return [0,[]] , []
        else :
            for occasion in occasions :
                if occasions.count(occasion) > luck[0] :
                    luck=[occasions.count(occasion),occasion]
            return luck,occasions

def get_action(cell,player_mill,player,state,rules) :
   mills=[]
   luck=True
   can_move=False
   can_go=[]
   board=state.get_board()
   player_mills=board.player_mills(player)
   cells=rules.get_effective_cell_moves(state,cell)

   if len(cells) != 0 :
        for mill_cell in player_mill :
            if mill_cell != cell :
                for x in rules.get_effective_cell_moves(state,mill_cell) :
                    can_go.append(x)

        if len(can_go) != 0 :
            for mill in board.mills() :
                for cell in cells :
                    if cell in mill and len([x for x in can_go if x in mill]) != 0:
                        mills.append(mill)

        if len(mills) != 0 :
             for mill in mills :
                for mill_cell in mill :
                    if mill_cell in board.get_player_pieces_on_board(Color(-1*player)) :
                        luck=False
                    if mill_cell in board.get_player_pieces_on_board(Color(player)) :
                        can_move=True
                if luck == True and can_move == True :
                   mill_cell=[x for x in mill if x in cells]
                   return mill_cell[0]
   return False


def are_same_color(rules,state,mills,player,cell) :
    board=state.get_board()
    pieces=board.get_player_pieces_on_board(Color(player))

    cells=rules.get_effective_cell_moves(state,cell)
    if len(cells) == 2 :
        return True
    elif len(cells) == 1 :
        if len(mills) == 2 :
            mill=[x for x in mills if cells[0] not in x][0]
            if mill[1] in pieces :
                return True
        if len(mills) == 1 :
            mill=mills[0]
            if mill.index(cell) in [0,2] :
                return True
            else :
                if mill[0] in pieces or mill[2] in pieces :
                    return True
    else :
        return False


def Make_occasion(rules,state,player,actions) :
    board=state.get_board()
    if actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.ADD :

        choice=ADD_and_Ocassion(state,player)
        
        for cell in choice :
            for action in actions :
                if action.get_action_as_dict()['action']['to'] == cell  :
                        return action
        return MorabarabaRules.random_play(state,player)
               
    elif actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.MOVE :
        pieces=board.get_player_pieces_on_board(Color(player))
        player_mills=board.player_mills(player)
        mills=board.mills()
        dont_move_cell=[]
        if can_make_mill(state,rules,player*-1) == False :

            for player_mill in player_mills :
                for mill_cell in player_mill :
                    new_mills=[mill for mill in mills if mill_cell in mill and mill != player_mill ]
                    luck=are_same_color(rules,state,new_mills,player,mill_cell)
                    if luck == True :
                        for action in actions :
                            if action.get_action_as_dict()['action']['at'] == mill_cell  :
                                return action

            for player_mill in player_mills :
                for mill_cell in player_mill :
                    luck=get_action(mill_cell,player_mill,player,state,rules)
                    if luck != False :
                        for action in actions :
                            if action.get_action_as_dict()['action']['at'] == mill_cell and  action.get_action_as_dict()['action']['to'] == luck :
                                return action
                    else :
                        dont_move_cell.append(mill_cell)
          
            choice=contracte(dont_move_cell,actions,state,rules,player)
            if choice != False :
                return choice
            
            return MorabarabaRules.random_play(state,player)
        else :
            for mill in player_mills :
                for mill_cell in mill :
                    dont_move_cell.append(mill_cell)
            
            choice=contracte(dont_move_cell,actions,state,rules,player)
            if choice != False :
                return choice

            return MorabarabaRules.random_play(state,player)
        return MorabarabaRules.random_play(state,player)
    else :
        return MorabarabaRules.random_play(state,player)

def contracte(dont_move_cell,actions,state,rules,player) :

    dont_do_action=[action for action in actions if action.get_action_as_dict()["action"]["at"] in dont_move_cell]

    if len(dont_move_cell) != 0 :
        new_actions=[new_action for new_action in actions if new_action.get_action_as_dict()["action"]['at'] not in dont_move_cell]
        if len(new_actions) != 0 :
            choice=which_move(state,rules,new_actions,player)
            if choice == False :
                choice=which_move(state,rules,dont_do_action,player)
                if choice == False :
                    choice=random_play(dont_do_action)
                    if choice == False :
                        choice=random_play(actions)
        else :
            choice=which_move(state,rules,dont_do_action,player)
            if choice == False :
                choice=random_play(dont_do_action)
                if choice == False :
                        choice=random_play(actions)
    else :
        choice=which_move(state,rules,actions,player)
        if choice == False :
            choice=random_play(actions)

    return choice    

def which_move(state,rules,actions,player) :
    board=state.get_board()
    for action in actions :
        old_board=state.get_board()
        board=old_board
        tmp=action.get_action_as_dict()
        at = tmp['action']['at']
        to = tmp['action']['to']
        board.empty_cell(at)
        board.fill_cell(to,Color(player))
        state.set_board(board)
        mills=is_making_mill(board,player*-1,at)
        if mills[0] != True or is_effective_making_mill(state,player*-1,rules,at,mills[1][0]) == False :
            state.set_board(old_board)
            return action

        state.set_board(old_board)
    return False            


class AI(MorabarabaPlayer):
    name = "SGCM"

    def __init__(self, color):  
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        try:
            rules=MorabarabaRules(self.position)
            board=state.get_board()
            actions=rules.get_player_actions(state,self.position)
            if actions[0].get_action_as_dict()["action_type"] == MorabarabaActionType.ADD :
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
            
        except:
            rules=MorabarabaRules(self.position)
            actions=rules.get_player_actions(state,self.position)
            return random.choice(actions)
            



def random_play(actions) :
    if len(actions) != 0 :
        print("\n\n random")
        return random.choice(actions)
    return False