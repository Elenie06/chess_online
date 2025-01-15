from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight 
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook

class Game :
    def __init__(self,id) :
        self.ready = False
        self.id = id 
        #initialisation du plateau de jeu
        self.board = [[Rook("white"),Knight("white"),Bishop("white"),Queen("white"),
                        King("white"),Bishop("white"),Knight("white"),Rook("white")] , 

                      [Pawn("white"),Pawn("white"),Pawn("white"),Pawn("white"),Pawn("white"),Pawn("white"),Pawn("white"),Pawn("white")] ,
                      [None]*8 ,[None]*8 ,
                      [None]*8,[None]*8 , 
                      [Pawn("black"),Pawn("black"),Pawn("black"),Pawn("black"),Pawn("black"),Pawn("black"),Pawn("black"),Pawn("black")]*8,
        
                      [Rook("black"),Knight("black"),Bishop("black"),Queen("black"),
                       King("black"),Bishop("black"),Knight("black"),Rook("black")]]
        #initialisaion des coups léguaux de toutes les pièces du plateau
        self.playing = 0
        self.last_move = -1
        for lign in range(8):
            for column in range(8) :
                try :
                    self.board[lign][column].update_legal_moves(self.board,[lign,column],self.last_move)  
                except :
                    pass
        self.play_piece = None
        self.selec = None
        self.winner = None
        self.colors = ["white","black"]
        self.playing_legal_moves = []
        self.promoted = None

    #gère le plateau de jeu et la logique de jeu
    def play(self,move) :
        try :
            self.selectioned,self.y,self.x = map(int,move.split())
        except :
            self.selectioned,self.y,self.x, self.promoted= map(int,move.split())
        #si on touche une piece
        if not self.selectioned :
            self.play_piece = self.board[self.x][self.y]
            self.selec = [self.x,self.y]
            self.playing_legal_moves = self.play_piece.legal_moves
        #si on a deja selectionné une piece
        elif self.x != self.selec[0] or self.y != self.selec[1] :
            if self.promoted != None :
                if self.promoted == 4 :
                    self.board[self.x][self.y] = Queen(self.colors[self.playing])
                elif self.promoted == 1 :
                    self.board[self.x][self.y] = Rook(self.colors[self.playing])
                elif self.promoted == 3:
                    self.board[self.x][self.y] = Bishop(self.colors[self.playing])
                elif self.promoted == 2 :
                    self.board[self.x][self.y] = Knight(self.colors[self.playing])
                self.board[self.selec[0]][self.selec[1]] = None
                self.promoted = None
                self.playing = abs(self.playing-1)
                self.update_all()
                self.selec = None

            #déplacement de la pièce si le coup est légal
            elif [self.x,self.y] in self.playing_legal_moves:
                self.was_there = self.board[self.x][self.y]
                self.board[self.x][self.y] = self.play_piece
                self.board[self.selec[0]][self.selec[1]] = None

                #en passant
                if self.was_there == None and self.play_piece.type == "pawn" and self.y != self.selec[1]:
                    self.board[self.selec[0]][self.y] = None
                if self.play_piece.type == "pawn" and abs(self.x-self.selec[0]) == 2 :
                    self.last_move = self.y
                else :
                    self.last_move = -1
                #roque
                if self.play_piece.type == "king":
                    self.board[self.x][self.y].hasnt_moved = False
                    if abs(self.y-self.selec[1]) == 2:
                        if self.y == 6 :
                            self.board[self.x][5] = self.board[self.x][7]
                            self.board[self.x][7] = None
                        else :
                            self.board[self.x][3] = self.board[self.x][0]
                            self.board[self.x][0] = None
                if self.play_piece.type == "rook" :
                    self.board[self.x][self.y].hasnt_moved = False
                self.playing = abs(self.playing-1)
                self.update_all()
                self.selec = None
            self.playing_legal_moves = []


    def update_all(self):
        #update legal moves de chaque piece
        stalemate = True
        for lign in range(8) :
            for column in range(8) :
                piece = self.board[lign][column]
                if piece != None :
                    piece.update_legal_moves(self.board,[lign,column],self.last_move) 
                    if piece.color_index == self.playing and piece.legal_moves != []:
                        stalemate = False
        if stalemate :
            self.reset(abs(self.playing-1))


    def connected(self) :
        return self.ready

    #gère la fin de partie
    def reset(self,winner) :
        self.stalemate = True
        for lign in range(8) :
            for column in range(8) :
                piece = self.board[lign][column]
                if piece != None :
                    if piece.color_index == winner :
                        for legal_move in piece.legal_moves:
                            if self.board[legal_move[0]][legal_move[1]] != None:
                                if self.board[legal_move[0]][legal_move[1]].type == "king":
                                    self.stalemate = False

        self.winner = "White" if winner == 0 else "Black"
        if self.stalemate:
            self.winner = "draw"