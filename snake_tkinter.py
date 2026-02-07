import tkinter as tk
import random


WIDTH = 500
HEIGHT = 500
CELL_SIZE = 20
SPEED = 150

root = tk.Tk()
root.title("Snake Game ")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()


score = 0
score_text = canvas.create_text(
    10, 10, fill="white", font=("Arial", 14),
    text="Score: 0", anchor="nw"
)

game_over_text = None
running = True

# Initial snake
snake = [(100, 100), (80, 100), (60, 100)]
direction = "Right"

# Food
def create_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return (x, y)

food = create_food()

def draw_food():
    canvas.delete("food")
    x, y = food
    canvas.create_oval(
        x, y, x + CELL_SIZE, y + CELL_SIZE,
        fill="red", tag="food"
    )

def draw_snake():
    canvas.delete("snake")
    for x, y in snake:
        canvas.create_rectangle(
            x, y, x + CELL_SIZE, y + CELL_SIZE,
            fill="green", tag="snake"
        )

def game_over():
    global running, game_over_text
    running = False
    game_over_text = canvas.create_text(
        WIDTH // 2, HEIGHT // 2,
        fill="white",
        font=("Arial", 24, "bold"),
        text="🐍bhag ja \nPress R to Restart",
        justify="center"
    )

def move_snake():
    global snake, food, score

    if not running:
        return

    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    else:
        new_head = (head_x + CELL_SIZE, head_y)

 
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        game_over()
        return

   
    if new_head in snake:
        game_over()
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 10
        canvas.itemconfig(score_text, text=f"Score: {score}")
        food = create_food()
        draw_food()
    else:
        snake.pop()

    draw_snake()
    root.after(SPEED, move_snake)

def change_direction(new_dir):
    global direction
    opposite = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }
    if opposite[new_dir] != direction:
        direction = new_dir

def restart_game(event=None):
    global snake, direction, score, running, food
    canvas.delete("all")

    score = 0
    running = True
    direction = "Right"
    snake = [(100, 100), (80, 100), (60, 100)]

    global score_text
    score_text = canvas.create_text(
        10, 10, fill="white", font=("Arial", 14),
        text="Score: 0", anchor="nw"
    )

    food = create_food()
    draw_food()
    draw_snake()
    move_snake()


root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))
root.bind("r", restart_game)
root.bind("R", restart_game)

draw_food()
draw_snake()
move_snake()

root.mainloop()
