import tensorflow as tf
import numpy as np
from base.model_V1_0.ChessSanLexer import ChessSanLexer as lexer
from base.model_V1_0.Piece_Keys import PieceKeys as pk


class TrainingData:
    white_turn: bool = True
    def __init__(self, san_chess_notation: list[str]) -> None:
        print(san_chess_notation)
        self.san_notation:  list[str] = san_chess_notation
        self.board = np.zeros((8, 8, 8), dtype=np.float32)  # pyright: ignore[reportUnannotatedClassAttribute]
        #self.board:_Array[tuple[int, int, int], np.float32]= np.zeros((8, 8, 8), dtype=np.float32)

    def update_board(self, lex: lexer) -> None:
        pos: str = lex.san_element
        L: int = len(pos)

        if 'O-O' in pos:
            if self.white_turn:
                self.board[6][0] += np.array(pk.King_Castle[0])
                self.board[5][0] += np.array(pk.Rook_Move[0])
            else:
                self.board[6][7] += np.array(pk.King_Castle[0])
                self.board[5][7] += np.array(pk.Rook_Move[0])
            return

        elif 'O-O-O' in pos:
            if self.white_turn:
                self.board[2][0] += np.array(pk.King_Castle[1])
                self.board[3][0] += np.array(pk.Rook_Move[1])
            else:
                self.board[2][7] += np.array(pk.King_Castle[1])
                self.board[3][7] += np.array(pk.Rook_Move[1])
            return

        elif pos[0] in ['N','B','R','Q','K']:
            pos = pos[L-3:L-1] if '+' in pos else pos[L-2:L]

        elif any(char in pos for char in ['N','B','R','Q','K']):
            pos = pos[L-4:L-2] if '+' in pos else pos[L-3:L-1]

        else:
            pos = pos[L-3:L-1] if '+' in pos else pos[L-2:L]
        
        print(pos)
        
        self.board[ ord(pos[0])-ord('a') ][ int(pos[1])-1 ] += np.array( lex.chess_piece[0] if self.white_turn else lex.chess_piece[1] )

    def san_to_tensorslices(self) -> list[tf.Tensor]:
        set: list[tf.Tensor] = []

        for index, element in enumerate(self.san_notation):
            if index == len(self.san_notation)-1:
                break

            lex: lexer = lexer(element)

            if not lex.san_is_valid:
                print(element)
                return set

            self.update_board(lex)
            self.white_turn = not self.white_turn
            set.append(tf.constant(self.board, dtype=tf.int16))

        return set