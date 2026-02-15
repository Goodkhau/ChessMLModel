class PieceKeys:
    Pawn_Move:      list[list[int]] = [[-6, 0,-5,-3,-7, 3, 8,-3], [ 8, 1,-4,-5,-4, 3,-7, 4]]
    Pawn_Capture:   list[list[int]] = [[-3, 3, 7, 1,-6,-4, 8,-4], [-7,-2, 5,-7, 8,-5,-7,-5]]
    Pawn_Promote:   list[list[int]] = [[ 0,-2, 1,-8, 5, 7, 5, 1], [ 3,-7, 6, 2,-1, 7, 8,-7]]
    Knight_Move:    list[list[int]] = [[ 5, 4, 5,-4, 0,-1,-3, 2], [-6,-8,-3, 1,-5,-7,-6, 0]]
    Knight_Capture: list[list[int]] = [[ 7,-6,-4, 3,-3, 7,-2,-3], [-6, 1,-2,-7,-1, 2,-6, 3]]
    Bishop_Move:    list[list[int]] = [[-5,-6,-1,-1, 2, 4,-5, 1], [-4, 7, 3,-2, 2, 0,-1,-6]]
    Bishop_Capture: list[list[int]] = [[-4,-2, 7,-3,-2,-8, 4, 5], [ 3, 1,-1,-3, 2,-7, 4,-8]]
    Rook_Move:      list[list[int]] = [[ 3, 2, 3, 7, 1, 2, 1, 5], [ 1, 2, 0,-4, 2,-3,-6,-8]]
    Rook_Capture:   list[list[int]] = [[-2,-5,-3, 6, 4,-4,-8, 0], [-3,-7,-1, 2, 2, 0, 1,-7]]
    Queen_Move:     list[list[int]] = [[-4,-5,-5,-7,-5, 7, 3,-8], [ 1,-8, 2,-6, 3, 5, 4, 4]]
    Queen_Capture:  list[list[int]] = [[-5,-7, 6, 5,-2, 0,-5,-4], [-1,-7,-7, 4,-5, 5, 3,-6]]
    Queen_Castle:   list[list[int]] = [[ 4,-8, 7,-3,-8,-2, 5, 7], [ 3, 6, 1,-8,-1,-5,-1,-8]]
    King_Move:      list[list[int]] = [[-7,-4,-6,-6,-8, 2,-7,-6], [ 7,-2,-8,-4,-1, 4,-6,-4]]
    King_Capture:   list[list[int]] = [[ 6,-1,-4,-3, 3,-8,-6,-8], [-7,-5,-7,-1, 0, 3,-4, 7]]
    King_Castle:    list[list[int]] = [[ 6,-1, 3,-6, 6, 2,-1,-6], [ 2,-5,-5, 5,-8,-5, 7, 2]]

    def get_chess_key_from_san(self, san_element: str) -> list[list[int]]:
        if san_element == 'O-O-O':
            return self.Queen_Castle
        if san_element == 'O-O':
            return self.King_Castle
            
        match (san_element[0]):
            case 'N':
                return self.Knight_Capture if 'x' in san_element else self.Knight_Move
            case 'B':
                return self.Bishop_Capture if 'x' in san_element else self.Bishop_Move
            case 'R':
                return self.Rook_Capture if 'x' in san_element else self.Rook_Move
            case 'Q':
                return self.Queen_Capture if 'x' in san_element else self.Queen_Move
            case 'K':
                return self.King_Capture if 'x' in san_element else self.King_Move
            case _:
                if any(char in san_element for char in ['N','B','R','Q','K']):
                    return self.Pawn_Promote
                return self.Pawn_Capture if 'x' in san_element else self.Pawn_Move