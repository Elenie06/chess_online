class King() :
    def __init__(self, color) :
        self.color = color
        self.color_index = 0 if self.color == "white" else 1
        self.hasnt_moved = True
        self.type = "king"
        self.type_index = 5

    def legal_move(self, board, start, end,last_move) :
        #case dans l'echiquier
        if not (0<=end[0]<=7 and 0<=end[1]<=7):
            return False
        #piece de meme couleur
        if board[end[0]][end[1]] != None:
            if self.color == board[end[0]][end[1]].color:
                return False
            
        if abs(start[0]-end[0]) <= 1 and abs(start[1]-end[1]) <= 1:
            return True

        #roque
        if self.hasnt_moved and board[end[0]][max(end[1],start[1])-1] == None:
            if self.color == "white" :
                if end[0] == 0 and end[1] == 6 and board[0][7]!=None:
                    if not self.check(board,start,end,last_move) and not self.check(board,start,start,last_move) and not self.check(board,start,[0,5],last_move) and board[0][7].type == "rook":
                        if board[0][7].hasnt_moved:
                            return True
                elif end[0] == 0 and end[1] == 2 and board[0][0]!=None:
                    if not self.check(board,start,end,last_move) and not self.check(board,start,start,last_move) and not self.check(board,start,[0,3],last_move) and board[0][0].type == "rook":
                        if board[0][0].hasnt_moved:
                            return True
            else :
                if end[0] == 7 and end[1] == 6 and board[7][7]!=None:
                    if not self.check(board,start,end,last_move) and not self.check(board,start,start,last_move) and not self.check(board,start,[7,5],last_move) and board[7][7].type == "rook":
                        if board[7][7].hasnt_moved:
                            return True
                elif end[0] == 7 and end[1] == 2 and board[7][0]!=None:
                    if not self.check(board,start,end,last_move) and not self.check(board,start,start,last_move) and not self.check(board,start,[7,3],last_move) and board[7][0].type == "rook":
                        if board[7][0].hasnt_moved:
                            return True
        return False
    
    def update_legal_moves(self,board,start,last_move) :
        self.legal_moves = []
        squares = [[1,1],[1,-1],[1,0],[-1,0],[-1,-1],[-1,1],[0,1],[0,-1],[0,2],[0,-2]]
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