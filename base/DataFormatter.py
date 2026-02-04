import tensorflow as tf
from base.ChessSanLexer import ChessSanLexer as lexer
from base.Piece_Keys import PieceKeys as pk


class TrainingData:
    white_turn: bool = True
    def __init__(self, san_chess_notation: list[str]) -> None:
        self.san_notation:  list[str] = san_chess_notation
        self.board:         list[list[list[int]]] = [[[0]*8]*8]*8

    def update_board(self, key: list[int]) -> None:
        return
    
    def san_to_tensorslices(self) -> list[tf.Tensor]:
        set: list[tf.Tensor] = []

        for element in self.san_notation:
            lex: lexer = lexer(element)
            if not lex.san_is_valid:
                continue

            self.update_board(lex.chess_piece[0])
            set.append(tf.constant(self.board, dtype=tf.int32))

        return set