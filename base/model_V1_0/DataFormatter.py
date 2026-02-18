import sys
import tensorflow as tf
import numpy as np
from base.model_V1_0.ChessSanLexer import ChessSanLexer as lexer
from base.model_V1_0.Piece_Keys import PieceKeys as pk


class TrainingData:
    white_turn: bool = True
    def __init__(self, san_chess_notation: list[str]) -> None:
        self.san_notation:  list[str] = san_chess_notation
        self.board = np.zeros((8, 8, 8), dtype=np.int16)  # pyright: ignore[reportUnannotatedClassAttribute]
    
    # Does not account for castling
    def get_position_from_san(self, san:str) -> str:
        L: int = len(san)-1 if '+' in san or '#' in san else len(san)
        if san[0] in ['N','B','R','Q','K']:
            return san[L-2:L]
        elif any(char in san for char in ['N','B','R','Q','K']):
            return san[L-4:L-2]
        else:
            return san[L-2:L]

    def update_board(self, lex: lexer) -> None:
        if 'O-O' == lex.san_element:
            if self.white_turn:
                self.board[6][0] += np.array(pk.King_Castle[0])
                self.board[5][0] += np.array(pk.Rook_Move[0])
            else:
                self.board[6][7] += np.array(pk.King_Castle[0])
                self.board[5][7] += np.array(pk.Rook_Move[0])
            return

        elif 'O-O-O' == lex.san_element:
            if self.white_turn:
                self.board[2][0] += np.array(pk.King_Castle[1])
                self.board[3][0] += np.array(pk.Rook_Move[1])
            else:
                self.board[2][7] += np.array(pk.King_Castle[1])
                self.board[3][7] += np.array(pk.Rook_Move[1])
            return

        position: str = self.get_position_from_san(san=lex.san_element)

        try:
            self.board[ ord(position[0])-ord('a') ][ int(position[1])-1 ] += np.array( lex.chess_piece[0] if self.white_turn else lex.chess_piece[1] )
        except ValueError:
            print("DataFormatter.py: Value Error: " + lex.san_element)
            sys.exit(1)
        except IndexError:
            print("DataFormatter.py: Index Error: " + position)
            sys.exit(1)


    def san_to_token_tensorslices(self) -> list[tf.Tensor]:
        features: list[tf.Tensor] = []

        for index, element in enumerate(self.san_notation):
            if index == len(self.san_notation)-1:
                break

            lex: lexer = lexer(element)

            if not lex.san_is_valid:
                print("DataFormatter.py: invalid san: " + element)
                return features

            self.update_board(lex)
            self.white_turn = not self.white_turn
            features.append(tf.constant(self.board, dtype=tf.int16, ))

        return features
    
    def san_to_label_tensorslices(self) -> list[tf.Tensor]:
        labels: list[tf.Tensor] = []

        for index, element in enumerate[str](self.san_notation):
            if index == 0:
                continue

            label = np.zeros((386), dtype=np.int8)

            if element == 'O-O' or element == 'O-O-O':
                pos = 0
            else:
                try:
                    position: str = self.get_position_from_san(san=element)
                    pos: int = 8*(ord(position[0])-ord('a')) + int(position[1])
                except ValueError:
                    print("DataFormatter.py: Value Error: " + element)
                    sys.exit(1)

            match (element[0]):
                case 'O':
                    if len(element) == 3:
                        label[384] = 1
                    else:
                        label[385] = 1
                case 'N':
                    label[1*64 + pos] = 1
                case 'B':
                    label[2*64 + pos] = 1
                case 'R':
                    label[3*64 + pos] = 1
                case 'Q':
                    label[4*64 + pos] = 1
                case 'K':
                    label[5*64 + pos] = 1
                case _:
                    label[0*64 + pos] = 1

            labels.append(tf.constant(label, dtype=tf.int8))

        return labels