class PieceKeys:
    Pawn_Move:     list[list[int]] = [[], []]
    Pawn_Capture:     list[list[int]] = [[], []]
    Pawn_Promote:     list[list[int]] = [[], []]
    Knight:   list[list[int]] = [[], []]
    Bishop:   list[list[int]] = [[], []]
    Rook:     list[list[int]] = [[], []]
    Queen:    list[list[int]] = [[], []]
    King:     list[list[int]] = [[], []]

    def get_chess_key_from_san(self, san_element: str) -> list[list[int]]:
        return self.Pawn