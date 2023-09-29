def task_16_1() -> list[list[str]]:
    board: list[list[str]] = []
    for i in range(0, 10):
        board.append(["🟦"] * 10)

    def can_place_ship(board, ship_length, start_row, start_col, orientation) -> bool:
        if orientation == 'horizontal':
            if start_col + ship_length > len(board[0]):
                return False
            for i in range(max(0, start_col - 1), min(len(board[0]), start_col + ship_length + 2)):
                for j in range(max(0, start_row - 1), min(len(board), start_row + 2)):
                    if board[j][i] == '⬜':
                        return False
        else:
            if start_row + ship_length > len(board):
                return False
            for i in range(max(0, start_col - 1), min(len(board[0]), start_col + 2)):
                for j in range(max(0, start_row - 1), min(len(board), start_row + ship_length + 2)):
                    if board[j][i] == '⬜':
                        return False
        return True

    def place_ship(board, ship_length) -> None:
        while True:
            orientation: str = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                start_row: int = random.randint(0, len(board) - 1)
                start_col: int = random.randint(0, len(board[0]) - ship_length)
                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    for i in range(ship_length):
                        board[start_row][start_col + i] = '⬜'
                    break
            else:
                start_row = random.randint(0, len(board) - ship_length)
                start_col = random.randint(0, len(board[0]) - 1)
                if can_place_ship(board, ship_length, start_row, start_col, orientation):
                    for i in range(ship_length):
                        board[start_row + i][start_col] = '⬜'
                    break

    for ship_length in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:
        place_ship(board, ship_length)
    return board

if __name__ == '__main__':
    main()
