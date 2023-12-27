from typing import Tuple, List, Set, Dict

Position = Tuple[int, int]

class Tetris:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.score = 0
        self.block: Dict[Position, Position] = {}
        self.fallen: Set[Position] = set()

    def get_score(self) -> int:
        return self.score

    def has_block(self) -> bool:
        if self.block:
            return True
        return False

    def __check_border(self, block: Dict[Position, Position]) -> bool:
        for tile, at in block.items():
            if at in self.fallen:
                return False
            if not self.__check_tile(at):
                return False
        return True

    def __check_tile(self, tile: Position) -> bool:
        x, y = tile
        return (0 <= x < self.cols and 0 <= y < self.rows)

    def add_block(self, block: List[Position],
                  col: int, row: int) -> bool:
        new_block: Dict[Position, Position] = {}
        for tile in block:
            x, y = tile
            new_block[tile] = (x + col, y + row)
        if self.__check_border(new_block):
            self.block = new_block
            return True
        return False

    def left(self) -> None:
        new_block: Dict[Position, Position] = {}
        for tile, at in self.block.items():
            col, row = at
            new_block[tile] = (col - 1, row)
        if self.__check_border(new_block):
            self.block = new_block

    def right(self) -> None:
        new_block: Dict[Position, Position] = {}
        for tile, at in self.block.items():
            col, row = at
            new_block[tile] = (col + 1, row)
        if self.__check_border(new_block):
            self.block = new_block

    def rotate_cw(self) -> None:
        result: List[Position] = []
        new_block: Dict[Position, Position] = {}

        cur_col, cur_row = self.block[(0, 0)]
        for tile in self.block.keys():
            x, y = tile
            result.append((-y, x))
        for tile in result:
            x, y = tile
            new_block[tile] = (x + cur_col, y + cur_row)
        if self.__check_border(new_block):
            self.block = new_block

    def rotate_ccw(self) -> None:
        result: List[Position] = []
        new_block: Dict[Position, Position] = {}

        cur_col, cur_row = self.block[(0, 0)]
        for tile in self.block.keys():
            x, y = tile
            result.append((y, -x))
        for tile in result:
            x, y = tile
            new_block[tile] = (x + cur_col, y + cur_row)
        if self.__check_border(new_block):
            self.block = new_block

    def __place(self) -> None:
        for tile, at in self.block.items():
            self.fallen.add(at)
        self.block = {}

    def __remove_rows(self) -> None:
        remove_rows: List[int] = []

        # finds full rows
        for row in range(self.rows):
            good_row: bool = True
            for col in range(self.cols):
                if (col, row) not in self.fallen:
                    good_row = False
            if good_row:
                remove_rows.append(row)

        # removes full rows from fallen
        self.score += len(remove_rows) ** 2

        fallen_list: List[Position] = []
        for tile in self.fallen:
            fallen_list.append(tile)
        for remove in remove_rows:
            removed: List[Position] = []
            for tile in fallen_list:
                col, row = tile
                if row != remove:
                    removed.append(tile)
            fallen_list = removed

        # moves down rest of the tiles
        for down in remove_rows:
            downed: List[Position] = []
            for tile in fallen_list:
                col, row = tile
                if row < down:
                    downed.append((col, row + 1))
                else:
                    downed.append(tile)
            fallen_list = downed

        self.fallen = set(fallen_list)

    def down(self) -> None:
        new_block: Dict[Position, Position] = {}
        for tile, at in self.block.items():
            x, y = at
            new_block[tile] = (x, y + 1)
        if self.__check_border(new_block):
            self.block = new_block
        else:
            self.__place()
            self.__remove_rows()

    def drop(self) -> None:
        while True:
            new_block: Dict[Position, Position] = {}
            for tile, at in self.block.items():
                col, row = at
                new_block[tile] = (col, row + 1)
            if self.__check_border(new_block):
                self.block = new_block
            else:
                break
        self.__place()
        self.__remove_rows()

    def tiles(self) -> List[Position]:
        result: List[Position] = []
        result = list(self.fallen)
        for tile, at in self.block.items():
            result.append(at)
        return result


def main() -> None:
    # tests
    tetris = Tetris(10, 22)

    assert tetris.get_score() == 0
    assert not tetris.has_block()
    assert tetris.tiles() == []

    block_s = [(1, -1), (0, -1), (0, 0), (-1, 0)]

    assert not tetris.add_block(block_s, 4, 0)
    assert not tetris.has_block()

    assert tetris.add_block(block_s, 4, 1)
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(3, 1), (4, 0), (4, 1), (5, 0)}
    assert len(tetris.tiles()) == 4

    tetris.down()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(3, 2), (4, 1), (4, 2), (5, 1)}
    assert len(tetris.tiles()) == 4

    tetris.left()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(2, 2), (3, 1), (3, 2), (4, 1)}
    assert len(tetris.tiles()) == 4

    tetris.right()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(3, 2), (4, 1), (4, 2), (5, 1)}
    assert len(tetris.tiles()) == 4

    tetris.right()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(4, 2), (5, 1), (5, 2), (6, 1)}
    assert len(tetris.tiles()) == 4

    tetris.rotate_cw()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(5, 1), (5, 2), (6, 2), (6, 3)}
    assert len(tetris.tiles()) == 4

    tetris.rotate_ccw()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(4, 2), (5, 1), (5, 2), (6, 1)}
    assert len(tetris.tiles()) == 4

    tetris.rotate_ccw()
    assert tetris.has_block()
    assert set(tetris.tiles()) == {(4, 1), (4, 2), (5, 2), (5, 3)}
    assert len(tetris.tiles()) == 4

    tetris.drop()
    assert not tetris.has_block()
    assert set(tetris.tiles()) == {(4, 19), (4, 20), (5, 20), (5, 21)}
    assert len(tetris.tiles()) == 4

    assert tetris.get_score() == 0
    assert block_s == [(1, -1), (0, -1), (0, 0), (-1, 0)]


if __name__ == '__main__':
    main()
