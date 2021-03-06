from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()
RED = (255, 0, 0)
BLUE = (0, 0, 255)
Green = (0, 255, 0)
White = (255, 255, 255)


lives = 3
x = 0
y = 4
lives_1 = 0
lives_2 = 1
lives_3 = 2
points = 0

game_over = False

matrix = [[BLUE for column in range(8)] for row in range(8)]
#draw_life = [[White for cloumn in range (0)]for row in range(0,2)]

def flatten(matrix):
    flattened = [pixel for row in matrix for pixel in row]
    return flattened


def gen_pipes(matrix):
    for row in matrix:
        row[-1] = RED
    gap = randint(1, 6)
    matrix[gap][-1] = BLUE
    matrix[gap - 1][-1] = BLUE
    matrix[gap + 1][-1] = BLUE
    return matrix


def move_pipes(matrix):
    for row in matrix:
        for i in range(7):
            row[i] = row[i + 1]
        row[-1] = BLUE
    return matrix


def draw_astronaut(event):
    global y
    global x
    sense.set_pixel(x, y, BLUE)
    if event.action == "pressed":
        if event.direction == "up" and y > 0:
            y -= 1
        elif event.direction == "down" and y < 7:
            y += 1
        elif event.direction == "right" and x < 7:
            x += 1
        elif event.direction == "left" and x > 0:
            x -= 1
    sense.set_pixel(x, y, Green)
    if matrix[y][x] == RED:
      game_over = True

    
def check_collision(matrix):
    if matrix[y][x] == RED:
        return True
    else:
        return False
    
sense.stick.direction_any = draw_astronaut

while not game_over:
    matrix = gen_pipes(matrix)
    if check_collision(matrix) == False:
        points = points + 1
        if points == 20:
            sense.show_message('You Win', text_colour = Green)
            points = points 
            lives = 1
            game_over = False
    
    if check_collision(matrix):
        game_over = True
        
    for i in range(2):
        matrix = move_pipes(matrix)
        sense.set_pixels(flatten(matrix))
        sense.set_pixel(x, y, Green)
    
        
        if check_collision(matrix):
            lives = lives - 1
            points = points -1 
        sleep(1)
        if lives == 0:
          sleep(1)
          game_over = True
          sleep(1)
        if points == -1:
            game_over = True
        while game_over:
              sense.show_message('You Lose',text_colour = RED)
              sense.show_message('Points: ' + str(points), text_colour = BLUE)
              sleep(1)
              points = 0
              lives = 3 
              game_over = False
