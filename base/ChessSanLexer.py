import re
from base.Piece_Keys import PieceKeys as pieces
from base.ChessSanRegex import Validator as vd

class ChessSanLexer:
    def __init__(self, san_element: str) -> None:
        pk = pieces()
        result: re.Match[str] | None = vd.valid_san.fullmatch(san_element)

        self.san_is_valid:  bool = True if result != None else False
        self.san_element:   str = san_element
        self.chess_piece:   list[list[int]] = pk.get_chess_key_from_san(san_element);
