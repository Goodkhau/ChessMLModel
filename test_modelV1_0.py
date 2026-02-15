import unittest
from base.model_V1_0.ChessSanLexer import ChessSanLexer as lexer
from base.model_V1_0.Piece_Keys import PieceKeys as pk
from base.model_V1_0.DataFormatter import TrainingData as formatter

test_game: list[str] = [
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
            lex = lexer(san)
            print(san)
            self.assertTrue(lex.san_is_valid)

class TestSanPieceMatch(unittest.TestCase):
    def test_piece_keys(self) -> None:
        self.assertEqual(pk.Pawn_Move, lexer(test_game[0]).chess_piece)
        self.assertEqual(pk.Queen_Capture, lexer(test_game[56]).chess_piece)
        self.assertEqual(pk.Pawn_Capture, lexer(test_game[31]).chess_piece)
        self.assertEqual(pk.Bishop_Move, lexer(test_game[5]).chess_piece)

class TestDataFormatter(unittest.TestCase):
    def test_formatter_feature(self) -> None:
        format = formatter(test_game)
        for index, element in enumerate(format.san_to_token_tensorslices()):
            if (index <= 1):
                print('Index ' + str(index) + ': Element')
                print(element)
            self.assertEqual(element.shape, (8, 8, 8))
    
    def test_formatter_label(self) -> None:
        format = formatter(test_game)
        for index, element in enumerate(format.san_to_label_tensorslices()):
            if (index <= 5):
                print('Index ' + str(index) + ': Element')
                print(element)
            self.assertEqual(element.shape, (386))
            self.assertTrue(sum(int(x) == 1 for x in element) == 1)
        
    def test_formatter_size(self) -> None:
        format = formatter(test_game)
        self.assertEqual(len(format.san_to_token_tensorslices()), len(test_game)-1)
        self.assertEqual(len(format.san_to_label_tensorslices()), len(test_game)-1)

    def test_board_update(self) -> None:
        for san in test_game:
            lex = lexer(san)
            pos: str = lex.san_element
            if 'O-O' in pos:
                self.assertEqual(lex.chess_piece, pk.King_Castle)

            elif 'O-O-O' in pos:
                self.assertEqual(lex.chess_piece, pk.Queen_Castle)

            elif pos[0] in ['N','B','R','Q','K']:
                self.assertTrue(any(lex.chess_piece == element for element in [pk.Knight_Move, pk.Knight_Capture, 
                                                                                    pk.Bishop_Move, pk.Bishop_Capture,
                                                                                    pk.Rook_Move,   pk.Rook_Capture,
                                                                                    pk.Queen_Move,  pk.Queen_Capture,
                                                                                    pk.King_Move,   pk.Queen_Capture]))

            elif any(char in pos for char in ['N','B','R','Q','K']):
                self.assertEqual(lex.chess_piece, pk.Pawn_Promote)

            else:
                self.assertTrue(any(lex.chess_piece == element for element in [pk.Pawn_Capture, pk.Pawn_Move]))

    def test_position_substr(self) -> None:
        for pos in test_game:
            L: int = len(pos)
            if pos[0] in ['N','B','R','Q','K']:
                pos = pos[L-3:L-1] if '+' in pos else pos[L-2:L]
            else:
                pos = pos[L-3:L-1] if '+' in pos else pos[L-2:L]
            print(pos)

    def test_indexing(self) -> None:
        pos: str = 'e4'
        self.assertEqual([ord(pos[0])-ord('a'), int(pos[1])-1], [4, 3])
        pos = 'a1'
        self.assertEqual([ord(pos[0])-ord('a'), int(pos[1])-1], [0, 0])
        pos = 'h8'
        self.assertEqual([ord(pos[0])-ord('a'), int(pos[1])-1], [7, 7])
        pos = 'c7'
        self.assertEqual([ord(pos[0])-ord('a'), int(pos[1])-1], [2, 6])

if __name__ == "__main__":
    _ = unittest.main()