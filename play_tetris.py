from random import choice
import tkinter as tk

# change f_tetris below if your file name is different
import game_logic as student

# game parameters; feel free to change them
ROWS = 22
COLS = 10
DELAY = 1000  # how often shall DOWN happen automatically; in milliseconds

BORDER = 32
CELL_SIZE = 32
FONT = ('system', '16')
TILE_COLOUR = 'blue'

LEFT, RIGHT, DOWN, DROP, ROTATE_CW, ROTATE_CCW, QUIT, RESTART = range(8)

EVENTS = {
    'a': LEFT,
    'Left': LEFT,
    'd': RIGHT,
    'Right': RIGHT,
    's': DOWN,
    'Down': DOWN,
    'space': DROP,
    'q': ROTATE_CCW,
    'Prior': ROTATE_CCW,
    'e': ROTATE_CW,
    'Next': ROTATE_CW,
    'x': QUIT,
    'r': RESTART,
}

SCORE_MSG = "Score: {}"
GO_MSG = 'Game over. Final score: {}.\nPress r to restart or x to quit.'

BLOCKS = [
    # I
    [(1, 0), (0, 0), (-1, 0), (-2, 0)],
    [(0, 1), (0, 0), (0, -1), (0, -2)],
    [(-1, 0), (0, 0), (1, 0), (2, 0)],
    [(0, -1), (0, 0), (0, 1), (0, 2)],
    # J
    [(0, -1), (0, 0), (0, 1), (-1, 1)],
    [(1, 0), (0, 0), (-1, 0), (-1, -1)],
    [(0, 1), (0, 0), (0, -1), (1, -1)],
    [(-1, 0), (0, 0), (1, 0), (1, 1)],
    # L
    [(1, 0), (0, 0), (-1, 0), (-1, 1)],
    [(0, 1), (0, 0), (0, -1), (-1, -1)],
    [(-1, 0), (0, 0), (1, 0), (1, -1)],
    [(0, -1), (0, 0), (0, 1), (1, 1)],
    # S
    [(-1, -1), (-1, 0), (0, 0), (0, 1)],
    [(1, -1), (0, -1), (0, 0), (-1, 0)],
    [(1, 1), (1, 0), (0, 0), (0, -1)],
    [(-1, 1), (0, 1), (0, 0), (1, 0)],
    # Z
    [(0, -1), (0, 0), (-1, 0), (-1, 1)],
    [(1, 0), (0, 0), (0, -1), (-1, -1)],
    [(0, 1), (0, 0), (1, 0), (1, -1)],
    [(-1, 0), (0, 0), (0, 1), (1, 1)],
    # T
    [(0, -1), (0, 0), (0, 1), (-1, 0)],
    [(1, 0), (0, 0), (-1, 0), (0, -1)],
    [(0, 1), (0, 0), (0, -1), (1, 0)],
    [(-1, 0), (0, 0), (1, 0), (0, 1)],
    # O
    [(0, 0), (-1, 0), (0, 1), (-1, 1)],
    [(0, 0), (0, -1), (-1, 0), (-1, -1)],
    [(0, 0), (1, 0), (0, -1), (1, -1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


class Game:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            width=2 * BORDER + (COLS + 2) * CELL_SIZE,
            height=4 * BORDER + (ROWS + 1) * CELL_SIZE,
        )

        self.draw_border()
        self.canvas.pack()

        self.root.bind_all('<Key>', self.key_event)

        self.reset()

    def draw_border(self) -> None:
        for x in BORDER, BORDER + (COLS + 1) * CELL_SIZE:
            self.canvas.create_rectangle(
                x, BORDER,
                x + CELL_SIZE, BORDER + (ROWS + 1) * CELL_SIZE,
                fill='black'
            )

        self.canvas.create_rectangle(
            BORDER, BORDER + ROWS * CELL_SIZE,
            BORDER + (COLS + 2) * CELL_SIZE, BORDER + (ROWS + 1) * CELL_SIZE,
            fill='black'
        )

    def reset(self) -> None:
        self.running = True
        self.tetris = student.Tetris(cols=COLS, rows=ROWS)
        self.handle = self.root.after(DELAY, self.fall)
        self.after_event()

    def stop(self) -> None:
        self.root.after_cancel(self.handle)
        self.running = False

    def fall(self) -> None:
        if self.running:
            self.tetris.down()
            self.handle = self.root.after(DELAY, self.fall)
            self.after_event()

    def key_event(self, ev: tk.Event) -> None:
        action = EVENTS.get(ev.keysym)

        if action is None:
            return

        if action == RESTART:
            self.reset()
            return

        if not self.running:
            if action == QUIT:
                self.root.destroy()
            return  # no reactions to other keys in stopped state

        if action == LEFT:
            self.tetris.left()
        elif action == RIGHT:
            self.tetris.right()
        elif action == DOWN:
            self.tetris.down()
        elif action == DROP:
            self.tetris.drop()
        elif action == ROTATE_CW:
            self.tetris.rotate_cw()
        elif action == ROTATE_CCW:
            self.tetris.rotate_ccw()
        elif action == QUIT:
            self.stop()
        else:
            assert False  # no other actions

        self.after_event()

    def after_event(self) -> None:
        if self.running and not self.tetris.has_block():
            block = choice(BLOCKS)
            row = -min(y for _, y in block)
            min_x = min(x for x, _ in block)
            max_x = max(x for x, _ in block)
            col = (COLS - 1 - min_x - max_x) // 2

            if not self.tetris.add_block(block, col, row):
                self.stop()

        self.draw()

    def draw(self) -> None:
        self.canvas.delete('content')

        for x, y in self.tetris.tiles():
            cx, cy = (BORDER + c * CELL_SIZE for c in (x + 1, y))
            self.canvas.create_rectangle(
                cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                fill=TILE_COLOUR, tags='content'
            )

        msg = SCORE_MSG if self.running else GO_MSG

        self.canvas.create_text(
            BORDER + (COLS + 2) * CELL_SIZE // 2,
            5 * BORDER // 2 + (ROWS + 1) * CELL_SIZE,
            text=msg.format(self.tetris.get_score()), font=FONT,
            tags='content'
        )


def main() -> None:
    game = Game()

    game.root.mainloop()


if __name__ == '__main__':
    main()
