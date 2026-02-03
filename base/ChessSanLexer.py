import re
from base.Piece_Keys import PieceKeys as pk

class ChessSanLexer:
    chess_piece: list[list[int]] = []

    def __init__(self, san_element: str) -> None:
        self.san_element: str = san_element
        self.san_is_valid: bool = 

    valid_san: re.Pattern[str] = re.compile(r"""
                                    (
                                        (O-O)\+?

                                      | (O-O-O)\+?

                                      | (0-0)\+?

                                      | (0-0-0)\+?

                                      | ([a-h]
                                            (x[a-h][1-8])
                                          | [1-8]
                                        [NBRQK]?\+?)

                                      | ([NBRQK]
                                        ([a-h][1-8])?
                                        x?[a-h][1-8])

                                      | (R[a-h]|[1-8]x?[a-h][1-8]\+?)
                                    )
                                    """, re.VERBOSE)