import random
import copy
import time

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    global count
    count = 0

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        global count
        drop_phase = False
        if count < 4:
            drop_phase = True   # TODO: detect drop phase

        alpha = float('-inf')
        beta = float('inf') 
        next_stage = self.succ(state, drop_phase)
        move = []
        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            
            max_stage = float('-inf')
            best = None
            for stage in next_stage:
                value = self.max_value(stage, 2, self.my_piece, alpha, beta)
                max_stage = max(max_stage, value)
                if max_stage == value:
                    best = stage
            
            for i in range(5):
                for j in range(5):
                    if state[i][j] != best[i][j]:
                        if state[i][j] != ' ':
                            source_row = i
                            source_col = j
                        else:
                            row = i
                            col = j
            
            move.insert(0, (row, col))
            move.insert(1, (source_row, source_col))
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        #(row, col) = (random.randint(0,4), random.randint(0,4))
        #while not state[row][col] == ' ':
        #   (row, col) = (random.randint(0,4), random.randint(0,4))
        
        
        max_stage = float('-inf')
        best = None
        for stage in next_stage:
            max_stage = max(max_stage, self.max_value(stage, 0, self.my_piece, alpha, beta))
            if max_stage == self.max_value(stage, 0, self.my_piece, alpha, beta):
                best = stage
                
        for i in range(5):
            for j in range(5):
                if state[i][j] != best[i][j]:
                    row = i
                    col = j

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        count += 1
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins       
        for i in range(2):
            for j in range(2):
                 if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j]==self.my_piece else -1
                
        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(2):
                 if state[4-i][j] != ' ' and state[4-i][j] == state[4-i-1][j+1] == state[4-i-2][j+2] == state[4-i-3][j+3]:
                    return 1 if state[4-i][j]==self.my_piece else -1
                
        # TODO: check 3x3 square corners wins
        for i in range(3):
            for j in range(3):
                 if state[i+1][j+1] == ' ' and state[i][j] != ' ' and state[i][j] == state[i+2][j] == state[i][j+2] == state[i+2][j+2]:
                    return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet

    def succ(self, state, phase):
        succ_list = []
        if phase:
            for i in range(4):
                for j in range(4):
                    if state[i][j] == ' ':
                        new = copy.deepcopy(state)
                        new[i][j] = self.my_piece
                        succ_list.append(new)        
        else:
            for i in range(4):
                for j in range(4):
                    if state[i][j] == self.my_piece:
                        for k in range(-1,2):
                            if i+k >= 0 and i+k <=4 and state[i+k][j] == ' ':
                                if k != 0:
                                    new = copy.deepcopy(state)
                                    new[i+k][j] = self.my_piece
                                    new[i][j] = ' '
                                    if not new in succ_list:
                                        succ_list.append(new)
                                        
                            if i+k >= 0 and i+k <=4 and j<=3 and state[i+k][j+1] == ' ':
                                new = copy.deepcopy(state)
                                new[i+k][j+1] = self.my_piece
                                new[i][j] = ' '
                                if not new in succ_list:
                                    succ_list.append(new)
                                    
                            if i+k >= 0 and i+k <=4 and j>=1 and state[i+k][j-1] == ' ':
                                new = copy.deepcopy(state)
                                new[i+k][j-1] = self.my_piece
                                new[i][j] = ' '
                                if not new in succ_list:
                                    succ_list.append(new)      
                                    
        return succ_list
        
    def heuristic_game_value(self, state):
        mid_3, edge_3, cor_3, skip_3, mid_2, edge_2, cor_mid_2, cor_edge_2 = 0.9,0.7,0.7,0.7,0.4,0.2,0.4,0.2
        if self.game_value(state)!= 0 :
            return self.game_value(state)
        
        #mid_3 + edge_3
        for i in range(5):
            for j in range(3):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1] == state[i][j+2]:
                    if j!=0:
                        return mid_3 if state[i][j]==self.my_piece else -1*mid_3
                    else:
                        return edge_3 if state[i][j]==self.my_piece else -1*edge_3
        for i in range(3):
            for j in range(5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i+2][j]:
                    if i!=0:
                        return mid_3 if state[i][j]==self.my_piece else -1*mid_3
                    else:
                        return edge_3 if state[i][j]==self.my_piece else -1*edge_3 
       
        for i in range(3):
            for j in range(3):
                 if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2]:
                    if i!=0 and j!=0:
                        return mid_3 if state[i][j]==self.my_piece else -1*mid_3
                    else:
                        return edge_3 if state[i][j]==self.my_piece else -1*edge_3
 
        for i in range(3):
            for j in range(3):
                 if state[4-i][j] != ' ' and state[4-i][j] == state[4-i-1][j+1] == state[4-i-2][j+2]:
                    if i!=0 and j!=0:
                        return mid_3 if state[4-i][j]==self.my_piece else -1*mid_3
                    else:
                        return edge_3 if state[4-i][j]==self.my_piece else -1*edge_3
         
        #core_3
        for i in range(3):
            for j in range(3):
                if state[i][j] == state[i+2][j] == state[i][j+2] or state[i][j] == state[i+2][j] == state[i+2][j+2] or state[i][j] == state[i][j+2] == state[i+2][j+2] or state[i+2][j] == state[i][j+2] == state[i+2][j+2]:
                        if state[i][j] != ' ':
                            return cor_3 if state[i][j]==self.my_piece else -1*cor_3
                        else: 
                            return cor_3 if state[i+2][j]==self.my_piece else -1*cor_3
            
        #skip_3 eg oo_o
        for i in range(5):
            for j in range(2):
                if state[i][j] != ' ':
                    if state[i][j] == state[i][j+1] == state[i][j+3] or state[i][j] == state[i][j+2] == state[i][j+3]:
                        return skip_3 if state[i][j]==self.my_piece else -1*skip_3
                    
        for i in range(2):
            for j in range(5):
                if state[i][j] != ' ':
                    if state[i][j] == state[i+1][j] == state[i+3][j] or state[i][j] == state[i+2][j] == state[i+3][j]:
                        return skip_3 if state[i][j]==self.my_piece else -1*skip_3
       
        for i in range(2):
            for j in range(2):
                 if state[i][j] != ' ':
                    if state[i][j] == state[i+1][j+1] == state[i+3][j+3] or state[i][j] == state[i+2][j+2] == state[i+3][j+3]:
                        return skip_3 if state[i][j]==self.my_piece else -1*skip_3
 
        for i in range(2):
            for j in range(2):
                 if state[4-i][j] != ' ':
                    if state[4-i][j] == state[3-i][j+1] == state[1-i][j+3] or state[4-i][j] == state[2-i][j+2] == state[1-i][j+3]:
                        return skip_3 if state[4-i][j]==self.my_piece else -1*skip_3
                 
        #mid_2 + edge_2
        for i in range(5):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1]:
                    if j!=0:
                        return mid_2 if state[i][j]==self.my_piece else -1*mid_2
                    else:
                        return edge_2 if state[i][j]==self.my_piece else -1*edge_2
        for i in range(4):
            for j in range(5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j]:
                    if i!=0:
                        return mid_2 if state[i][j]==self.my_piece else -1*mid_2
                    else:
                        return edge_2 if state[i][j]==self.my_piece else -1*edge_2 
       
        for i in range(4):
            for j in range(4):
                 if state[i][j] != ' ' and state[i][j] == state[i+1][j+1]:
                    if i!=0 and j!=0:
                        return mid_2 if state[i][j]==self.my_piece else -1*mid_2
                    else:
                        return edge_2 if state[i][j]==self.my_piece else -1*edge_2
 
        for i in range(4):
            for j in range(4):
                 if state[4-i][j] != ' ' and state[4-i][j] == state[4-i-1][j+1]:
                    if i!=0 and j!=0:
                        return mid_2 if state[4-i][j]==self.my_piece else -1*mid_2
                    else:
                        return edge_2 if state[4-i][j]==self.my_piece else -1*edge_2
                    
        #cor_mid_2 + cor_edge_2
        for i in range(3):
            for j in range(3):
                if state[i][j] == state[i+2][j] or state[i][j] == state[i][j+2] or state[i][j] == state[i+2][j+2]:
                        if state[i][j] == state[i+2][j] and j == 2:
                            return cor_mid_2 if state[i][j]==self.my_piece else -1*cor_mid_2
                        elif state[i][j] == state[i][j+2] and i == 2:
                            return cor_mid_2 if state[i][j]==self.my_piece else -1*cor_mid_2
                        else: 
                            return cor_edge_2 if state[i][j]==self.my_piece else -1*cor_edge_2
         
        return 0 
    
    def max_value(self, state, depth, player, alpha, beta):
        if self.game_value(state)!= 0 :
            return self.game_value(state)
                
        elif depth == 0:
            return self.heuristic_game_value(state)
        
        if player == self.my_piece:
            value = float('-inf')
            for s in self.succ(state, False):
                value = max(value, self.max_value(s, depth-1, self.opp, alpha, beta))
                alpha = max(alpha, self.max_value(s, depth-1, self.opp, alpha, beta))
                if beta <= alpha:
                    break
                return value
        else:
            value = float('inf')
            for s in self.succ(state, False):
                value = min(value, self.max_value(s, depth-1, self.my_piece, alpha, beta))
                beta = min(beta, self.max_value(s, depth-1, self.my_piece, alpha, beta))
                if beta <= alpha:
                    break
                return value
    
############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

   
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
