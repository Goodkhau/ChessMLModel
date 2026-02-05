class PieceKeys:
    Pawn_Move:      list[list[int]] = [[], []]
    Pawn_Capture:   list[list[int]] = [[], []]
    Pawn_Promote:   list[list[int]] = [[], []]
    Knight_Move:    list[list[int]] = [[], []]
    Knight_Capture: list[list[int]] = [[], []]
    Bishop_Move:    list[list[int]] = [[], []]
    Bishop_Capture: list[list[int]] = [[], []]
    Rook_Move:      list[list[int]] = [[], []]
    Rook_Capture:   list[list[int]] = [[], []]
    Queen_Move:     list[list[int]] = [[], []]
    Queen_Capture:  list[list[int]] = [[], []]
    Queen_Castle:   list[list[int]] = [[], []]
    King_Move:      list[list[int]] = [[], []]
    King_Capture:   list[list[int]] = [[], []]
    King_Castle:    list[list[int]] = [[], []]

    def get_chess_key_from_san(self, san_element: str) -> list[list[int]]:
        match (san_element[0]):
            case 'N':
                return self.Knight_Capture if 'x' in san_element else self.Knight_Move
            case 'B':
                return self.Bishop_Capture if 'x' in san_element else self.Bishop_Move
            case 'R':
                return self.Rook_Capture if 'x' in san_element else self.Rook_Move
            case 'Q':
                if san_element == 'O-O-O':
                    return self.Queen_Castle
                return self.Queen_Capture if 'x' in san_element else self.Queen_Move
            case 'K':
                if san_element == 'O-O':
                    return self.King_Castle
                return self.King_Capture if 'x' in san_element else self.King_Move
            case _:
                if any(char in san_element for char in ['N','B','R','Q','K']):
                    return self.Pawn_Promote
                return self.Pawn_Capture if 'x' in san_element else self.Pawn_Move