import random
import pyxel
from pathlib import Path

CELL_SIZE = 8
GRID_W = 16 #grid width
GRID_H = 16 #grid height

SCREEN_W = GRID_W * CELL_SIZE
SCREEN_H = GRID_H * CELL_SIZE

TITLE = 0
PLAYING = 1
GAME_OVER = 2


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Retro Snake", fps=30)

        #pyxel.load("/home/emma/ProjectsM/snake.pyxres") #sprites and resources custom
        resource_file = Path(__file__).parent / "snake.pyxres"
        pyxel.load(str(resource_file))

        self.high_score = 0
        self.state = TITLE

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.snake = [(8, 8), (7, 8), (6, 8)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0

        self.move_timer = 0
        self.move_delay = 6

        self.spawn_food()
        self.state = PLAYING

    def spawn_food(self):
        while True:
            food = (
                random.randint(0, GRID_W - 1),
                random.randint(0, GRID_H - 1),
            )

            if food not in self.snake:
                self.food = food
                return

    def handle_input(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.direction != (0, 1):
            self.next_direction = (0, -1)

        elif pyxel.btnp(pyxel.KEY_DOWN) and self.direction != (0, -1):
            self.next_direction = (0, 1)

        elif pyxel.btnp(pyxel.KEY_LEFT) and self.direction != (1, 0):
            self.next_direction = (-1, 0)

        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.direction != (-1, 0):
            self.next_direction = (1, 0)

    def move_snake(self):
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy,
        )

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_W
            or new_head[1] < 0
            or new_head[1] >= GRID_H
        ):
            self.state = GAME_OVER
            return

        # Self collision
        if new_head in self.snake:
            self.state = GAME_OVER
            return

        self.snake.insert(0, new_head)

        # Food eaten
        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)

            # Speed up gradually
            self.move_delay = max(2, 6 - self.score // 5)

            self.spawn_food()
        else:
            self.snake.pop()

    def update(self):
        if self.state == TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return

        if self.state == GAME_OVER:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = TITLE
            return

        self.handle_input()

        self.move_timer += 1

        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.move_snake()
            return

        
    def draw_grid(self):
        for x in range(0, SCREEN_W, CELL_SIZE):
            pyxel.line(x, 0, x, SCREEN_H, 1)

        for y in range(0, SCREEN_H, CELL_SIZE):
            pyxel.line(0, y, SCREEN_W, y, 1)

    def draw_snake(self):

        # ---------- HEAD ----------
        hx, hy = self.snake[0]

        dx, dy = self.direction

        w = 8
        h = 8

        if (dx, dy) == (-1, 0):      # left
            w = -8

        elif (dx, dy) == (0, -1):    # up
            h = -8

        elif (dx, dy) == (0, 1):     # down
            w = -8
            h = -8

        pyxel.blt(
            hx * CELL_SIZE,
            hy * CELL_SIZE,
            0,
            0, 0,
            w, h,
            0
        )

        # ---------- BODY ----------
        for i in range(1, len(self.snake) - 1):

            x, y = self.snake[i]

            prev_x, prev_y = self.snake[i - 1]
            next_x, next_y = self.snake[i + 1]

            # Vertical body
            if prev_x == next_x:

                pyxel.blt(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    0,
                    0, 24,     # vertical body
                    8, 8,
                    0
                )

            else:

                pyxel.blt(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    0,
                    16, 0,     # horizontal body
                    8, 8,
                    0
                )
        # ---------- TAIL ----------
        tail = self.snake[-1]
        before_tail = self.snake[-2]

        tx, ty = tail

        dx = tail[0] - before_tail[0]
        dy = tail[1] - before_tail[1]

        if dx != 0:

            w=8 if dx > 0 else -8

            pyxel.blt(
                tx * CELL_SIZE,
                ty * CELL_SIZE,
                0,
                40, 0,
                w, 8,
                0
            )
        else:
            h=8 if dy > 0 else -8
            pyxel.blt(
                tx * CELL_SIZE,
                ty * CELL_SIZE,
                0,
                48, 0,
                8, h,
                0
            )

    def draw_title(self):
        pyxel.cls(0)

        pyxel.text(44, 35, "RETRO SNAKE", 11)

        if pyxel.frame_count % 30 < 15:
            pyxel.text(32, 70, "PRESS SPACE TO START", 7)

        pyxel.text(42, 95, f"BEST SCORE {self.high_score}", 6)

    def draw_game_over(self):
        pyxel.cls(0)

        pyxel.text(46, 40, "GAME OVER", 8)

        pyxel.text(42, 60, f"SCORE {self.score}", 7)

        pyxel.text(
            24,
            85,
            "PRESS SPACE FOR TITLE",
            6,
        )

    def draw(self):

        if self.state == TITLE:
            self.draw_title()
            return

        if self.state == GAME_OVER:
            self.draw_game_over()
            return
        
        pyxel.cls(1)

        pyxel.bltm(
            0, 0,   # screen position
            0,         # tilemap number
            0, 0,   # tilemap coordinates
            SCREEN_W, SCREEN_H
        )
        #self.draw_grid()
        self.draw_snake()

       

        # Food
        ax, ay = self.food

        pyxel.blt(
            ax * CELL_SIZE, ay * CELL_SIZE,
            0,
            40, 16,
            8, 8,
            0
        )

        # UI
        pyxel.text(2, 2, f"SCORE {self.score}", 7)
        pyxel.text(2, 10, f"BEST  {self.high_score}", 7)

    
        

App()