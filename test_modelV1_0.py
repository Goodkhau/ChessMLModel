import unittest
from base.model_V1_0.ChessSanLexer import ChessSanLexer as lexer
from base.model_V1_0.Piece_Keys import PieceKeys as pk

test_game = [
    "e4","d6","d4","g6","Nc3",
    "Bg7","f4","a6","e5","b5",
    "Qf3","c6","Bd3","Nh6","h3",
    "Nf5","Nce2","h5","g4","hxg4",
    "hxg4","Rxh1","Qxh1","Nh6","g5",
    "Nf5","Qh7","Kf8","Nh3","c5",
    "c3","cxd4","cxd4","dxe5","Bxf5",
    "Bxf5","dxe5","Qd7","Nf2","Nc6",
    "Bd2","e6","Be3","Qe7","Rc1",
    "Qb4+","Kf1","Qxb2","Rxc6","Qb1+",
    "Rc1","Qxa2","Bc5+","Ke8","Qg8+",
    "Kd7","Qxf7+","Kc6","Be3+","Kd5",
    "Nc3+"
]

class TestSanLexer(unittest.TestCase):
    def test_lexer(self) -> None:
        for san in test_game:
            print(san)
            lex = lexer(san)
            self.assertTrue(lex.san_is_valid)

class TestSanPieceMatch(unittest.TestCase):
    def test_piece_keys(self) -> None:
        self.assertEqual(pk.Pawn_Move, lexer(test_game[0]).chess_piece)
        self.assertEqual(pk.Queen_Capture, lexer(test_game[56]).chess_piece)
        self.assertEqual(pk.Pawn_Capture, lexer(test_game[31]).chess_piece)
        self.assertEqual(pk.Bishop_Move, lexer(test_game[5]).chess_piece)

# if __name__ == "__main__":
#     _ = unittest.main()