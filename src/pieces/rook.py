class Rook() :
    def __init__(self, color) :
        self.color = color
        self.color_index = 0 if self.color == "white" else 1
        self.hasnt_moved = True
        self.type = "rook"
        self.type_index = 1
        
    def legal_move(self, board, start, end,last_move) :
        #case dans l'echiquier
        if not (0<=end[0]<=7 and 0<=end[1]<=7):
            return False
        #piece de meme couleur
        if board[end[0]][end[1]] != None:
            if self.color == board[end[0]][end[1]].color:
                return False
            
        if start[0] == end[0]:
            if start[1] > end[1] :
                gap = -1
            else :
                gap = 1
            for i in range(abs(start[1]-end[1])-1):
                if board[start[0]][start[1]+i*gap+gap] != None :
                    return False
            return True

        elif start[1] == end[1] :
            if start[0] > end[0] :
                gap = -1
            else :
                gap = 1
            for i in range(abs(start[0]-end[0])-1):
                if board[start[0]+i*gap+gap][start[1]] != None :
                    return False
            return True
        return False
        
    def update_legal_moves(self,board,start,last_move) :
        self.legal_moves = []
        for move in [[1,0], [-1,0], [0,-1], [0,1]]:
            end = [0,0]
            while 0<=end[0]+start[0]<=7 and 0<=end[1]+start[1]<=7 :
                test = [start[0]+end[0],start[1]+end[1]]
                if self.legal_move(board,start,test,last_move):
                    if not self.check(board,start,test,last_move):
                        self.legal_moves.append(test)
                end[0] += move[0]
                end[1] += move[1]
                

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