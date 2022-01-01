import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


import random
import pygame as pg

 
WHITE  = (255, 255, 255)
L_GREY = (217, 217, 217) 
BLACK  = (0, 0, 0)

SNAKE_COLOR = WHITE
APPLE_COLOR = WHITE


class Snake:
    def __init__(self):
        self.segments  = []
        self.direction = ''
        self._create_head()

    def _create_head(self):
        x = 200
        y = 200

        self.segments.append({'x':x, 'y':y})
        for i in range(3):
            x += -11 if x-(i*11) <= 400 else 11
            self.segments.append({'x':x, 'y':y})

        self.direction = 'W' if x-(33) <= 400 else 'E'

    def draw(self, surface):
        for seg in self.segments:
            outline = pg.Rect(seg['x'], seg['y'], 11, 11)
            body    = pg.Rect(seg['x'], seg['y'], 10, 10)

            pg.draw.rect(surface, SNAKE_COLOR, body)
            pg.draw.rect(surface, BLACK, outline, 1)

    def move(self, key):
        match key:
            case pg.K_w | pg.K_UP:
                if self.direction != 'S': 
                    self.direction = 'N'
            case pg.K_d | pg.K_RIGHT:
                if self.direction != 'W':
                    self.direction = 'E'
            case pg.K_s | pg.K_DOWN:
                if self.direction != 'N':
                    self.direction = 'S'
            case pg.K_a | pg.K_LEFT:
                if self.direction != 'E':
                    self.direction = 'W'

    def update(self):
        self.add_segment(0)
        self.segments.pop(-1)

    def add_segment(self, index=-1):
        x = 10 if self.direction == 'E' else -10 if self.direction == 'W' else 0
        y = 10 if self.direction == 'S' else -10 if self.direction == 'N' else 0

        new = {
                'x': self.segments[index]['x'] + x,
                'y': self.segments[index]['y'] + y
              }
        self.segments.insert(index, new)

    def collision(self):
        x, y = list(self.segments[0].values())

        if x >= 400 or x < 0:
            return 1
        if y >= 460 or y < 60:
            return 1

        for i in range(len(self.segments)-1):
            if x == self.segments[i+1]['x'] and y == self.segments[i+1]['y']:
                   return 1
        return 0


class Apple:
    def __init__(self):
        self.x    = (random.randrange(0, 400) // 10) * 10
        self.y    = (random.randrange(60, 460) // 10) * 10
        self.rect = pg.Rect(self.x, self.y, 10, 10)

    def draw(self, surface):
        outline = pg.Rect(self.x, self.y, 11, 11)
        body    = pg.Rect(self.x, self.y, 10, 10)

        pg.draw.rect(surface, APPLE_COLOR, body)
        pg.draw.rect(surface, BLACK, outline, 1)

    def collision(self, snake):
        if snake.segments[0]['x'] == self.x and\
           snake.segments[0]['y'] == self.y:
               return 1
        return 0


class Text:
    def __init__(self, text, size, x, y, color=WHITE):
        font      = pg.font.SysFont('Verdana.ttf', size)
        self.text = font.render(text, True, color)
        self.x    = x
        self.y    = y
        self.rect = self.text.get_rect()

    def draw(self, surface):
        self.rect.center = (self.x, self.y)
        surface.blit(self.text, self.rect)


class Button:
    def __init__(self, x, y, width, height, text, size=18, color=L_GREY, c_color=WHITE):
        self.text    = Text(text, size, x+(width/2), y+(height/2), BLACK)
        self.rect    = pg.Rect(x, y, width, height)
        self.x       = x
        self.y       = y
        self.width   = width
        self.height  = height
        self.d_color = color
        self.p_color = color
        self.c_color = c_color

    def draw(self, surface):
        pg.draw.rect(surface, self.d_color, self.rect)
        self.text.draw(surface)

    def update(self, mouse):
        if self.x + self.width >= mouse.x >= self.x and self.y + self.height >= mouse.y >= self.y:
            self.d_color = self.c_color

            if mouse.clicked == 1:
                return 1
            return 0

        self.d_color = self.p_color
        return 0


class TextArea:
    def __init__(self, x, y, width, height):
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height
        self.area   = Button(x, y, width, height, '')
        self.text   = ''
        self.active = 0

    def draw(self, surface, mouse):
        self.area.text = Text(self.text, 15, self.x+(self.width/2), self.y+(self.height/2), BLACK)

        if self.area.update(mouse):
            self.active = 1
        elif mouse.x < self.x or mouse.x > self.x+self.width and mouse.y < self.y or mouse.y > self.y+self.height:
            if mouse.clicked == 1:
                self.active = 0

        if self.active:
            self.area.d_color = self.area.c_color
        else:
            self.area.d_color = self.area.p_color

        self.area.draw(surface)

    def type(self, event):
        if not self.active:
            return 0

        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            return 0

        if event.key == pg.K_RETURN:
            self.state = 0
            return 1

        self.text += event.unicode
        return 0


class Mouse:
    x       = 0
    y       = 0
    clicked = 0


class Game:
    def __init__(self):
        """
            The classic arcade snake game built in pygame
        """

        pg.init()
        pg.display.set_caption('Snake Arcade')

        self.surface = pg.display.set_mode((400, 460))
        self.clock   = pg.time.Clock()
        self.mouse   = Mouse()

    def run(self):
        global SNAKE_COLOR, APPLE_COLOR

        # Create the snake and apple object
        snake      = Snake()
        apple      = Apple()
        color_btn  = Button(300, 20, 60, 20, 'Colors')
        score      = 0
        high_score = 0

        # Game over text
        game_over = Text('Game Over!', 40, 200, 120)
        spawn_btn = Button(125, 170, 150, 30, 'Try Again')

        # Settings objects
        snake_text  = Text('Snake color', 25, 110, 170)
        snake_tarea = TextArea(170, 160, 80, 20)
        apple_text  = Text('Apple color', 25, 110, 200) 
        apple_tarea = TextArea(170, 190, 80, 20)
        apply_btn   = Button(125, 300, 150, 30, 'Apply Settings')

        state = 'alive'
        while True:
            self.clock.tick(10)

            score_text      = Text(f'Score: {score}', 30, 200, 30)
            high_score_text = Text(f'High Score: {high_score}', 30, 200, 240)

            self.mouse.clicked         = pg.mouse.get_pressed()[0]
            self.mouse.x, self.mouse.y = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    snake.move(event.key)
                    snake_tarea.type(event)
                    apple_tarea.type(event)
            
            self.surface.fill(BLACK)

            if state == 'alive':
                pg.draw.rect(self.surface, WHITE, pg.Rect(0, 60, 400, 2))

                # Update snake's position
                snake.update()

                # Collision detection
                if apple.collision(snake):
                    apple  = Apple()
                    score += 1
                    snake.add_segment()

                if snake.collision():
                    state = 'game_over'
                    if score > high_score:
                        high_score = score
                
                if color_btn.update(self.mouse):
                    state = 'settings'
    
                # Draw sprites
                snake.draw(self.surface)
                apple.draw(self.surface)
                score_text.draw(self.surface)
                color_btn.draw(self.surface)
            elif state == 'game_over':
                if spawn_btn.update(self.mouse):
                    self.mouse.clicked = 0
                    state = 'alive'
                    snake = Snake()
                    apple = Apple()
                    score = 0

                game_over.draw(self.surface) 
                spawn_btn.draw(self.surface)
                high_score_text.draw(self.surface)
            elif state == 'settings':
                if apply_btn.update(self.mouse):
                    state = 'alive'
                    snake = Snake()
                    apple = Apple()
                    score = 0

                    s_color = snake_tarea.text.split(',')
                    a_color = apple_tarea.text.split(',')
                    if len(s_color) != 3 or len(a_color) != 3:
                        continue
                    SNAKE_COLOR = [int(i) for i in s_color]
                    APPLE_COLOR = [int(i) for i in a_color]

                snake_text.draw(self.surface)
                snake_tarea.draw(self.surface, self.mouse)
                apple_text.draw(self.surface)
                apple_tarea.draw(self.surface, self.mouse)
                apply_btn.draw(self.surface)

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
