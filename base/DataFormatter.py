import tensorflow as tf
import re
from base.ChessSanLexer import Validator as vld
from base.Piece_Keys import PieceKeys as pk


class TrainingData:
    white_turn: bool = True
    def __init__(self, san_chess_notation: list[str]) -> None:
        self.san_notation:  list[str] = san_chess_notation
        self.board:         list[list[list[int]]] = [[[0]*8]*8]*8

    def san_pattern_match(self, element: str) -> None:
        result: re.Match[str] | None = vld.valid_san.match(element)
        if result == None or result.start() != 0 or result.end() != len(element)-1:
            print("Invalid SAN: " + element)
            return

        match (len(element)):
            case 2:
                self.move(element)
            case 3:
                if element == '0-0' or element == 'O-O':
                    self.castle(element)
                else:
                    self.move(element)
            case 4:

            case 5:
                self.castle(element)
            case _:
                print("Unknown notation: " + element)

    
    def san_to_tensorslices(self) -> list[tf.Tensor]:
        set: list[tf.Tensor] = []

        for element in self.san_notation:
            self.san_pattern_match(element)
            set.append(tf.constant(self.board, dtype=tf.int32))

        return set