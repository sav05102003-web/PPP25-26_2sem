from enum import Enum
from typing import List, Tuple, Optional

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class Position:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Position) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

class Move:
    def __init__(self, from_pos: Position, to_pos: Position):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def __repr__(self):
        return f"Move({self.from_pos.row},{self.from_pos.col} -> {self.to_pos.row},{self.to_pos.col})"

class Piece:
    def __init__(self, color: Color):
        self.color = color
        self.has_moved = False

    def get_symbol(self) -> str:
        raise NotImplementedError

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        raise NotImplementedError

    def can_move_to(self, board: 'Board', from_pos: Position, to_pos: Position) -> bool:
        valid_moves = self.get_valid_moves(board, from_pos)
        return any(move.to_pos == to_pos for move in valid_moves)

class Pawn(Piece):
    def get_symbol(self) -> str:
        return "P" if self.color == Color.WHITE else "p"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1

        new_pos = Position(pos.row + direction, pos.col)
        if board.is_valid_position(new_pos) and not board.get_piece(new_pos):
            moves.append(Move(pos, new_pos))

            if pos.row == start_row:
                double_pos = Position(pos.row + 2 * direction, pos.col)
                if not board.get_piece(double_pos):
                    moves.append(Move(pos, double_pos))

        for col_offset in (-1, 1):
            attack_pos = Position(pos.row + direction, pos.col + col_offset)
            if (board.is_valid_position(attack_pos) and
                board.get_piece(attack_pos) and
                board.get_piece(attack_pos).color != self.color):
                moves.append(Move(pos, attack_pos))
        return moves

class Rook(Piece):
    def get_symbol(self) -> str:
        return "R" if self.color == Color.WHITE else "r"


    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_row, new_col = pos.row + dr * step, pos.col + dc * step
                new_pos = Position(new_row, new_col)
                if not board.is_valid_position(new_pos):
                    break
                piece = board.get_piece(new_pos)
                if not piece:
                    moves.append(Move(pos, new_pos))
                elif piece.color != self.color:
                    moves.append(Move(pos, new_pos))
                    break
                else:
                    break
        return moves

class Gryphon(Piece):
    def get_symbol(self) -> str:
        return "G" if self.color == Color.WHITE else "g"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr1, dc1 in knight_moves:
            jump_pos = Position(pos.row + dr1, pos.col + dc1)
            if not board.is_valid_position(jump_pos):
                continue
            if board.get_piece(jump_pos):  
                continue

            for dr2, dc2 in [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                             (0, 1), (1, -1), (1, 0), (1, 1)]:
                final_pos = Position(jump_pos.row + dr2, jump_pos.col + dc2)
                if (board.is_valid_position(final_pos) and
                    not board.get_piece(final_pos)):
                    moves.append(Move(pos, final_pos))
        return moves

class Phoenix(Piece):
    def get_symbol(self) -> str:
        return "F" if self.color == Color.WHITE else "f"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # вертикали/горизонтали
                   (1, 1), (1, -1), (-1, 1), (-1, -1)]  # диагонали

        for dr, dc in directions:
            for step in range(1, 4):  
                new_row, new_col = pos.row + dr * step, pos.col + dc * step
                new_pos = Position(new_row, new_col)

                if not board.is_valid_position(new_pos):
                    break

                piece = board.get_piece(new_pos)
                if not piece:
                    moves.append(Move(pos, new_pos))
                elif piece.color != self.color:
                    moves.append(Move(pos, new_pos))
                    break  
                else:
                    break  
        return moves

class Unicorn(Piece):
    def get_symbol(self) -> str:
        return "U" if self.color == Color.WHITE else "u"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr1, dc1 in knight_moves:
            first_jump = Position(pos.row + dr1, pos.col + dc1)
            if (not board.is_valid_position(first_jump) or
                board.get_piece(first_jump)):  
                continue

            for dr2, dc2 in knight_moves:
                second_jump = Position(first_jump.row + dr2, first_jump.col + dc2)
                if (board.is_valid_position(second_jump) and
                    not board.get_piece(second_jump)):
                    moves.append(Move(pos, second_jump))
        return moves


class Knight(Piece):
    def get_symbol(self) -> str:
        return "N" if self.color == Color.WHITE else "n"


    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            new_pos = Position(pos.row + dr, pos.col + dc)
            if board.is_valid_position(new_pos):
                piece = board.get_piece(new_pos)
                if not piece or piece.color != self.color:
                    moves.append(Move(pos, new_pos))
        return moves

class Bishop(Piece):
    def get_symbol(self) -> str:
        return "B" if self.color == Color.WHITE else "b"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            for step in range(1, 8):
                new_row, new_col = pos.row + dr * step, pos.col + dc * step
                new_pos = Position(new_row, new_col)
                if not board.is_valid_position(new_pos):
                    break
                piece = board.get_piece(new_pos)
                if not piece:
                    moves.append(Move(pos, new_pos))
                elif piece.color != self.color:
                    moves.append(Move(pos, new_pos))
                    break
                else:
                    break
        return moves

class Queen(Piece):
    def get_symbol(self) -> str:
        return "Q" if self.color == Color.WHITE else "q"


    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        return rook.get_valid_moves(board, pos) + bishop.get_valid_moves(board, pos)


class King(Piece):
    def get_symbol(self) -> str:
        return "K" if self.color == Color.WHITE else "k"

    def get_valid_moves(self, board: 'Board', pos: Position) -> List[Move]:
        moves = []
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            new_pos = Position(pos.row + dr, pos.col + dc)
            if board.is_valid_position(new_pos):
                piece = board.get_piece(new_pos)
                if not piece or piece.color != self.color:
                    moves.append(Move(pos, new_pos))
        return moves

class MoveHistoryEntry:
    def __init__(self, move: Move, captured_piece: Optional[Piece],
                 moved_piece: Piece, previous_turn: Color):
        self.move = move
        self.captured_piece = captured_piece
        self.moved_piece = moved_piece
        self.previous_turn = previous_turn


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_initial_position()
        self.history = []

    def _setup_initial_position(self):
        for col in range(8):
            self.grid[1][col] = Pawn(Color.BLACK)
            self.grid[6][col] = Pawn(Color.WHITE)

        back_row_pieces = [
            Rook,      # a1/a8
            Knight,    # b1/b8
            Bishop,    # c1/c8
            Gryphon,   # d1/d8 — вместо ферзя
            King,      # e1/e8
            Unicorn,   # f1/f8 — вместо слона
            Knight,    # g1/g8
            Rook       # h1/h8
        ]
        for col, piece_class in enumerate(back_row_pieces):
            self.grid[0][col] = piece_class(Color.BLACK)
            self.grid[7][col] = piece_class(Color.WHITE)

    def is_valid_position(self, pos: Position) -> bool:
        return 0 <= pos.row < 8 and 0 <= pos.col < 8

    def get_piece(self, pos: Position) -> Optional[Piece]:
        if self.is_valid_position(pos):
            return self.grid[pos.row][pos.col]
        return None

    def set_piece(self, pos: Position, piece: Optional[Piece]):
        if self.is_valid_position(pos):
            self.grid[pos.row][pos.col] = piece

    def move_piece(self, move: Move) -> bool:
        piece = self.get_piece(move.from_pos)
        if not piece:
            return False

        if piece.can_move_to(self, move.from_pos, move.to_pos):
            self.set_piece(move.to_pos, piece)
            self.set_piece(move.from_pos, None)
            piece.has_moved = True
            return True
        return False

    def display(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    print(piece.get_symbol(), end=" ")
                else:
                    print(".", end=" ")
            print()

    def move_piece(self, move: Move) -> bool:
        piece = self.get_piece(move.from_pos)
        if not piece:
            return False

        if piece.can_move_to(self, move.from_pos, move.to_pos):
            captured = self.get_piece(move.to_pos)
            entry = MoveHistoryEntry(move, captured, piece, self.current_color)
            self.history.append(entry)

            self.set_piece(move.to_pos, piece)
            self.set_piece(move.from_pos, None)
            piece.has_moved = True
            return True
        return False

    def undo_last_move(self) -> bool:
        if not self.history:
            return False

        entry = self.history.pop()
        move = entry.move

        self.set_piece(move.from_pos, entry.moved_piece)
        self.set_piece(move.to_pos, entry.captured_piece)

        entry.moved_piece.has_moved = False

        return True

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_color = Color.WHITE
        self.game_over = False

    def switch_turn(self):
        self.current_color = Color.BLACK if self.current_color == Color.WHITE else Color.WHITE

    def make_move(self, from_pos: str, to_pos: str) -> bool:
        from_row, from_col = self._parse_position(from_pos)
        to_row, to_col = self._parse_position(to_pos)

        from_position = Position(from_row, from_col)
        to_position = Position(to_row, to_col)

        move = Move(from_position, to_position)
        piece = self.board.get_piece(from_position)

        if (piece and piece.color == self.current_color and
                self.board.move_piece(move)):
            self.switch_turn()
            return True
        return False

    def _parse_position(self, pos_str: str) -> Tuple[int, int]:
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        return row, col

    def undo_move(self, steps: int = 1) -> bool:
        for _ in range(steps):
            if not self.board.undo_last_move():
                return False
        self.switch_turn()  
        return True

    def play(self):
        print("Добро пожаловать в шахматы! Введите ход в формате 'e2 e4'")
        print("Команды: 'undo N' — откатить N ходов, 'quit' — выход")
        while not self.game_over:
            self.board.display()
            print(f"Ход {self.current_color.value}:")
            move_input = input("Введите ход: ").strip()

            if move_input.lower() == 'quit':
                break
            elif move_input.startswith('undo'):
                try:
                    steps = int(move_input.split()[1]) if len(move_input.split()) > 1 else 1
                    if self.undo_move(steps):
                        print(f"Откат {steps} хода(ов) выполнен!")
                    else:
                        print("Невозможно выполнить откат.")
                except (IndexError, ValueError):
                    print("Неверный формат команды undo. Используйте 'undo' или 'undo N'.")
            else:
                try:
                    from_pos, to_pos = move_input.split()
                    if self.make_move(from_pos, to_pos):
                        print("Ход выполнен!")
                    else:
                        print("Неверный ход, попробуйте снова.")
                except ValueError:
                    print("Неверный формат хода. Используйте формат 'e2 e4'.")
                                      


    def play(self):
        print("Добро пожаловать в шахматы! Введите ход в формате 'e2 e4'")
        while not self.game_over:
            self.board.display()
            print(f"Ход {self.current_color.value}:")
            move_input = input("Введите ход: ").strip()

            if move_input.lower() == 'quit':
                break

            try:
                from_pos, to_pos = move_input.split()
                if self.make_move(from_pos, to_pos):
                    print("Ход выполнен!")
                else:
                    print("Неверный ход, попробуйте снова.")
            except ValueError:
                print("Неверный формат хода. Используйте формат 'e2 e4'.")

class CheckersPiece(Piece):
    def __init__(self, color: Color, is_king: bool = False):
        super().__init__(color)
        self.is_king = is_king

    def get_symbol(self) -> str:
        symbol = "O" if self.color == Color.WHITE else "o"
        return symbol.upper() if self.is_king else symbol

    def get_valid_moves(self, board: 'CheckersBoard', pos: Position) -> List[Move]:
        moves = []
        directions = [(-1, -1), (-1, 1)] if self.color == Color.WHITE or self.is_king else [(1, -1), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = pos.row + dr, pos.col + dc
            new_pos = Position(new_row, new_col)

            if board.is_valid_position(new_pos) and not board.get_piece(new_pos):
                moves.append(Move(pos, new_pos))

            jump_row, jump_col = pos.row + 2 * dr, pos.col + 2 * dc
            jump_pos = Position(jump_row, jump_col)
            middle_pos = Position(pos.row + dr, pos.col + dc)

            middle_piece = board.get_piece(middle_pos)
            if (board.is_valid_position(jump_pos) and
                not board.get_piece(jump_pos) and
                middle_piece and middle_piece.color != self.color):
                moves.append(Move(pos, jump_pos))
        return moves

class CheckersBoard(Board):
    def _setup_initial_position(self):
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = CheckersPiece(Color.BLACK)

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = CheckersPiece(Color.WHITE)

class CheckersGame:
    def __init__(self):
        self.board = CheckersBoard()
        self.current_color = Color.WHITE
        self.game_over = False

    def switch_turn(self):
        self.current_color = Color.BLACK if self.current_color == Color.WHITE else Color.WHITE

    def make_move(self, from_pos: str, to_pos: str) -> bool:
        from_row, from_col = self._parse_position(from_pos)
        to_row, to_col = self._parse_position(to_pos)

        from_position = Position(from_row, from_col)
        to_position = Position(to_row, to_col)

        move = Move(from_position, to_position)
        piece = self.board.get_piece(from_position)

        if (piece and piece.color == self.current_color and
                self.board.move_piece(move)):
            if (self.current_color == Color.WHITE and to_row == 0) or \
               (self.current_color == Color.BLACK and to_row == 7):
                if isinstance(piece, CheckersPiece):
                    piece.is_king = True
            self.switch_turn()
            return True
        return False

    def _parse_position(self, pos_str: str) -> Tuple[int, int]:
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        return row, col

    def play(self):
        print("Добро пожаловать в шашки! Введите ход в формате 'c3 d4'")
        while not self.game_over:
            self.board.display()
            print(f"Ход {self.current_color.value}:")
            move_input = input("Введите ход: ").strip()

            if move_input.lower() == 'quit':
                break

            try:
                from_pos, to_pos = move_input.split()
                if self.make_move(from_pos, to_pos):
                    print("Ход выполнен!")
                else:
                    print("Неверный ход, попробуйте снова.")
            except ValueError:
                print("Неверный формат хода. Используйте формат 'c3 d4'.")



if __name__ == "__main__":
    print("Выберите игру:")
    print("1 — Шахматы")
    print("2 — Шашки")

    choice = input("Ваш выбор (1, 2): ").strip()

    if choice == "1":
        game = ChessGame()
        game.play()
    elif choice == "2":
        game = CheckersGame()
        game.play()
    else:
        print("Неверный выбор. Запускаю шахматы по умолчанию.")
        game = ChessGame()
        game.play()

