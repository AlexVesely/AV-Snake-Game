from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 50
BODY_PARTS = 3
BACKGROUND_COLOR = "#000000"
SNAKE_COLOR = "#00FF00"

speed = 80
score = 0
high_score = 0
direction = 'down'
game_running = False # Flag to track if game is running
food_choice = "apple"
difficulty_choice = "medium"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x,y]

    def draw(self, color):
        canvas.create_oval(self.coordinates[0], self.coordinates[1], self.coordinates[0] + SPACE_SIZE,
                           self.coordinates[1] + SPACE_SIZE, fill=color, tag="food")

class Apple(Food):
    def __init__(self):
        super().__init__()
        self.color = "red"

    def draw(self):
        super().draw(self.color)

class Lemon(Food):
    def __init__(self):
        super().__init__()
        self.color = "yellow"

    def draw(self):
        super().draw(self.color)

class Orange(Food):
    def __init__(self):
        super().__init__()
        self.color = "orange"

    def draw(self):
        super().draw(self.color)

def create_fruit():
    global food_choice
    fruit_classes = {'apple': Apple, 'lemon': Lemon, 'orange': Orange}
    return fruit_classes[food_choice]()

def next_turn(snake, food):
    global speed
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE

    snake.coordinates.insert(0, (x,y))

    square_color = SNAKE_COLOR

    if food_choice == "orange":
        square_color = random.choice(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])

    snake_square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=square_color)

    snake.squares.insert(0, snake_square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, high_score, speed

        score += 1
        score_label.config(text="Score: {}".format(score))

        if score > high_score:
            high_score = score
            hs_label.config(text="High Score: {}".format(score))

        if food_choice == "lemon":
            speed = random.randint(50,100)

        canvas.delete("food")
        food = create_fruit()
        food.draw()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('small fonts', 110), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 100,
                       font=('small fonts', 20), text="Press Enter to Play Again", fill="white", tag="restart")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 200,
                       font=('small fonts', 20), text="Press 'm' to go Back to Start Menu", fill="white", tag="restart")
    window.bind('<Return>', set_game)
    window.bind('m', lambda event: start_menu())

def set_game(event=None):
    window.unbind('<Return>')
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))

    canvas.delete(ALL)
    global score, direction
    score = 0
    direction = 'down'
    score_label.config(text="Score: {}".format(score))

    snake = Snake()
    food = create_fruit()
    food.draw()

    next_turn(snake, food)

def center_window(window):
    # Update window to get accurate dimensions
    window.update()

    # Get current window dimensions
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate new position for centering the window
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    # Set new window geometry by knowing the windows width and height and centre of screen
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

def start_menu():
    canvas.delete(ALL)
    window.unbind('m')
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 250,
                           font=('small fonts', 100), text="AV Snake Game", fill="white", tag="startmenu")


    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 120,
                           font=('small fonts', 40), text="Choose a fruit:", fill="white", tag="startmenu")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 75,
                           font=('small fonts', 20), text="Press 'a' for apple, 'b' for lemon, 'c' for orange",
                           fill="white", tag="startmenu")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
                       font=('small fonts', 20), text=f"Fruit: {food_choice}", fill="green", tag="selection")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50,
                           font=('small fonts', 40), text="Choose a difficulty:", fill="white", tag="startmenu")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 100,
                           font=('small fonts', 20), text="Press '1' for easy, '2' for medium, '3' for hard",
                           fill="white", tag="startmenu")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 140,
                           font=('small fonts', 20), text=f"Difficulty: {difficulty_choice}", fill="green",
                           tag="selection")


    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 250,
                           font=('small fonts', 40), text="Press Enter to Start", fill="white", tag="startmenu")

    window.bind('<a>', select_fruit)
    window.bind('<b>', select_fruit)
    window.bind('<c>', select_fruit)

    window.bind('<KeyPress-1>', select_difficulty)
    window.bind('<KeyPress-2>', select_difficulty)
    window.bind('<KeyPress-3>', select_difficulty)

    window.bind('<Return>', set_game)

def select_fruit(event):
    global food_choice
    if event.char == 'a':
        food_choice = 'apple'
    elif event.char == 'b':
        food_choice = 'lemon'
    elif event.char == 'c':
        food_choice = 'orange'
    update_start_menu()

def select_difficulty(event):
    global difficulty_choice, speed
    if event.char == '1':
        speed = 120
        difficulty_choice = 'easy'
    elif event.char == '2':
        speed = 80
        difficulty_choice = 'medium'
    elif event.char == '3':
        speed = 50
        difficulty_choice = 'hard'
    update_start_menu()

def update_start_menu():
    canvas.delete("selection")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
                       font=('small fonts', 20), text=f"Fruit: {food_choice}", fill="green", tag="selection")

    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 140,
                           font=('small fonts', 20), text=f"Difficulty: {difficulty_choice}", fill="green", tag="selection")

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score_label = Label(window, text="Score: {}".format(score), font=('small fonts', 20))
score_label.pack()

hs_label = Label(window, text="High Score: {}".format(high_score), font=('small fonts', 20))
hs_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

center_window(window)

start_menu()

# Starts Tkinter event loop, which waits for user interactions and keeps the window open until closed
window.mainloop()
