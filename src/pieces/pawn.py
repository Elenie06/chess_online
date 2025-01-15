class Pawn() :
    def __init__(self, color) :
        self.color = color
        self.color_index = 0 if self.color == "white" else 1

        self.type = "pawn"
        self.type_index = 0


    def legal_move(self, board, start, end, last_move) :
        #case dans l'echiquier
        if not (0<=end[0]<=7 and 0<=end[1]<=7):
            return False
        #piece de meme couleur
        if board[end[0]][end[1]] != None:
            if self.color == board[end[0]][end[1]].color:
                return False
        #poussée
        if start[1] == end[1] and board[end[0]][end[1]] == None:
            if board[start[0]][start[1]].color == 'white' :
                if start[0] == 1 and end[0]-start[0] == 2 and board[2][start[1]] == None:
                    return True
                elif end[0]-start[0] == 1:
                    return True
            else :
                if start[0] == 6 and end[0]-start[0] == -2 and board[5][start[1]] == None:
                    return True
                elif end[0]-start[0] == -1:
                    return True      
        #prise
        elif abs(start[1]-end[1]) == 1 and board[end[0]][end[1]] != None:
            if board[start[0]][start[1]].color == 'white' :
                if end[0]-start[0] == 1:
                    return True
            else :
                if end[0]-start[0] == -1:
                    return True
        #en passant
        elif abs(start[1]-end[1]) == 1 and last_move == end[1] :
            if board[start[0]][start[1]].color == 'white' :
                if start[0] == 4 :
                    return True
            else :
                if start[0] == 3:
                    return True
        return False


    def update_legal_moves(self,board,start,last_move) :
        self.legal_moves = []
        if self.color == 'white' :
            squares = [[1,1],[1,-1],[1,0],[2,0]]
        else :
            squares = [[-1,-1],[-1,1],[-1,0],[-2,0]]
        for end_square in squares :
            end = [start[0]+end_square[0],start[1]+end_square[1]]
            if self.legal_move(board,start,end,last_move):
                if not self.check(board,start,end,last_move):
                    self.legal_moves.append(end)
        

    def check(self,board,start,end,last_move):
        board2 = []
        for lign in range(8):
            board2.append([])
            for column in range(8):
                board2[lign].append(board[lign][column])
        board2[start[0]][start[1]] = None
        board2[end[0]][end[1]] = self
        for lign in range(8):
            for column in range(8):
                try:
                    if board2[lign][column].type == "king" and board2[lign][column].color == self.color:
                        king = [lign,column]
                except:
                    pass
        for lign in range(8):
            for column in range(8):
                try:
                    if board2[lign][column].color != self.color:
                        if board2[lign][column].legal_move(board2,[lign,column],king,last_move) :
                            return True
                except:
                    pass
        return False