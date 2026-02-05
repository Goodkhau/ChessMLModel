import tensorflow as tf
from base.ChessSanLexer import ChessSanLexer as lexer


class TrainingData:
    white_turn: bool = True
    def __init__(self, san_chess_notation: list[str]) -> None:
        self.san_notation:  list[str] = san_chess_notation
        self.board:         list[list[list[int]]] = [[[0]*8]*8]*8

    def update_board(self, lex: lexer) -> None:
        pos: str = lex.san_element
        L: int = len(pos)

        if pos[0] in ['N','B','R','Q','K']:
            pos = pos[L-4:L-2] if '+' in pos else pos[L-3:L-1]
        else:
            pos = pos[L-4:L-2] if '+' in pos else pos[L-3:L-1]
        
        self.board[ ord(pos[0])-97 ][ int(pos[1]) ] += ( lex.chess_piece[0] if self.white_turn else lex.chess_piece[1] )

    def san_to_tensorslices(self) -> list[tf.Tensor]:
        set: list[tf.Tensor] = []

        for index, element in enumerate(self.san_notation):
            if index == len(self.san_notation)-1:
                break

            lex: lexer = lexer(element)

            if not lex.san_is_valid:
                return set

            self.update_board(lex)
            set.append(tf.constant(self.board, dtype=tf.int32))

        return set