import random as rd
import tkinter as Tk


# GLOBAL CONSTANTS:
FRAMES_PER_SECOND = 5 # The number of snake updates per second.
TILE_WIDTH = 42 # The width of each tile on the game board.
X_TILES = 15 # The number of horizontal tiles on the board, not including the border.
Y_TILES = 15 # The number of vertical tiles on the board, not including the border.
WIDTH = TILE_WIDTH * X_TILES + 2 * TILE_WIDTH # The overall width of the game window.
HEIGHT = TILE_WIDTH * Y_TILES + 2 * TILE_WIDTH # The overall height of the game window.
BORDER_COLOR = "black" # The color of the border.
BG_COLOR = "white" # The color of where the snake moves around.
APPLE_COLOR = "green" # The color of an Apple.
SNAKE_COLOR = "red" # The color of the Snake.
GAME_OVER_COLOR = "orange" # The color of a SnakeNode that causes gameover.
TEXT_COLOR = "black" # The color of displayed text.


class Apple:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.shape = self.canvas.create_oval(self.x * TILE_WIDTH, self.y * TILE_WIDTH, (self.x + 1) * TILE_WIDTH, (self. y + 1) * TILE_WIDTH, fill=APPLE_COLOR)


class SnakeNode:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.shape = self.canvas.create_rectangle(self.x * TILE_WIDTH, self.y * TILE_WIDTH, (self.x + 1) * TILE_WIDTH, (self.y + 1) * TILE_WIDTH, fill=SNAKE_COLOR)


class Snake:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.nodes = [SnakeNode(self.canvas, self.x, self.y)]
        # dir is the direction:
        # -1 is not moving, 0 is right, 1 is up, 2 is left, 3 is down
        # Initialize the Snake as standing still to make it more user friendly.
        self.dir = -1
    
    def contains(self, x, y):
        """
        Returns True if the Snake contains a SnakeNode at the grid position (x, y),
        otherwise returns False.
        """
        for node in self.nodes:
            if node.x == x and node.y == y:
                return True
        return False
    
    def set_dir(self, dir):
        """
        Sets the Snake's direction to dir as long as the Snake's length is 1
        or if dir is not the direction of the SnakeNode directly behind the head.
        Direction 0 is right, 1 is up, 2 is left, and 3 is down
        I will refer to the second node in the list of nodes as the "neck node"
        since it is directly behind the head.
        """
        if len(self.nodes) == 1:
            self.dir = dir
        # Calculate the tile difference in the x and y direction
        # between the head node and the neck node to make sure
        # that dir is not in the direction of the neck node.
        else:
            x_diff = self.nodes[0].x - self.nodes[1].x
            y_diff = self.nodes[0].y - self.nodes[1].y
            # To set the direction to right, the head node can't have an x
            # coordinate that is 1 below the neck node or else it will
            # cause a self collision with the neck node, which is annoying
            # to the player if they hit the wrong button.
            if dir == 0 and x_diff != -1:
                self.dir = dir
            # If dir is up and the neck node is not directly above the head,
            # set the direction to up.
            elif dir == 1 and y_diff != 1:
                self.dir = dir
            # the next 2 cases are the opposites of the last 2
            elif dir == 2 and x_diff != 1:
                self.dir = dir
            elif dir == 3 and y_diff != -1:
                self.dir = dir
    
    def move_and_check_for_collision(self) -> bool:
        """
        Moves the snake in the current direction. Returns True
        if the snake was able to successfully move without colliding,
        and False if it was not able to.
        """
        collided = False
        if self.dir == 0:
            self.x += 1
            if self.x == X_TILES + 1:
                collided = True
        elif self.dir == 1:
            self.y -= 1
            if self.y == 0:
                collided = True
        elif self.dir == 2:
            self.x -= 1
            if self.x == 0:
                collided = True
        elif self.dir == 3:
            self.y += 1
            if self.y == Y_TILES + 1:
                collided = True
        if self.contains(self.x, self.y):
            collided = True
        self.nodes = [SnakeNode(self.canvas, self.x, self.y)] + self.nodes
        return collided
    
    def pop_tail_node(self):
        tail_node = self.nodes[-1]
        self.canvas.delete(tail_node.shape)
        del self.nodes[-1]
        return tail_node
    
    def is_moving(self):
        return self.dir != -1
    
class Game:
    def __init__(self, master):
        self.active = True # Boolean value determining if the game is running.
        self.master = master
        # Create background.
        self.canvas = Tk.Canvas(master, width=WIDTH, height=HEIGHT, bg=BORDER_COLOR)
        # Create area for snake.
        self.canvas.create_rectangle(TILE_WIDTH, TILE_WIDTH, WIDTH - TILE_WIDTH, HEIGHT - TILE_WIDTH, fill=BG_COLOR)
        self.spawn_snake()
        self.spawn_apple()
        self.canvas.focus_set()
        self.canvas.bind("<Right>", lambda event: self.set_snake_dir(0))
        self.canvas.bind("<Up>", lambda event: self.set_snake_dir(1))
        self.canvas.bind("<Left>", lambda event: self.set_snake_dir(2))
        self.canvas.bind("<Down>", lambda event: self.set_snake_dir(3))
        self.canvas.bind("<Key>", self.reset())
        self.canvas.pack()
        self.move()

    def spawn_snake(self):
        """
        Spawns the snake at a random tile.
        """
        self.snake = Snake(self.canvas, rd.randint(1, X_TILES), rd.randint(1, Y_TILES))

    def delete_snake(self):
        """
        Deletes the snake from the canvas.
        """
        for node in self.snake.nodes:
            self.canvas.delete(node.shape)

    def spawn_apple(self):
        """
        Spawns an apple on the canvas and ensures that it is not in collision with the snake.
        """
        new_x = rd.randint(1, X_TILES)
        new_y = rd.randint(1, X_TILES)
        while self.snake.contains(new_x, new_y):
            new_x = rd.randint(1, X_TILES)
            new_y = rd.randint(1, X_TILES)
        self.apple = Apple(self.canvas, new_x, new_y)

    def delete_apple(self):
        """
        Deletes the apple from the canvas.
        """
        self.canvas.delete(self.apple.shape)
    
    def set_snake_dir(self, dir):
        """
        This function is only here to allow the arrow keys
        to be able to reset the game after a game over.
        """
        if self.active:
            self.snake.set_dir(dir)
        else:
            self.reset()

    def is_snake_colliding_with_apple(self):
        """
        Returns whether or not the snake is colliding with the apple.
        """
        return self.snake.x == self.apple.x and self.snake.y == self.apple.y
    
    def reset(self):
        """
        Resets the game after a game over.
        """
        if not self.active:
            self.active = True
            self.delete_game_over_messages()
            self.delete_snake()
            self.spawn_snake()
            self.delete_apple()
            self.spawn_apple()

    
    def display_game_over_message(self):
        """
        Displays the game over message at the end of the game.
        """
        self.game_over_message1 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Game over! Final length: {len(self.snake.nodes)}", fill="black")
        self.game_over_message2 = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text="Press any key to play again!", fill="black")
    

    def delete_game_over_messages(self):
        self.canvas.delete(self.game_over_message1)
        self.canvas.delete(self.game_over_message2)

    def make_snake_head_orange(self):
        self.canvas.delete(self.snake.nodes[0].shape)
        self.snake.nodes[0].shape = self.canvas.create_rectangle(self.snake.nodes[0].x * TILE_WIDTH, self.snake.nodes[0].y * TILE_WIDTH, (self.snake.nodes[0].x + 1) * TILE_WIDTH, (self.snake.nodes[0].y + 1) * TILE_WIDTH, fill=GAME_OVER_COLOR)

    def move(self):
        """
        The game loop. If the game is running then it moves the
        snake, checks for collisions, and handles game over.
        """
        if self.active:
            if self.snake.is_moving():
                tail_node = self.snake.pop_tail_node()
                in_collision = self.snake.move_and_check_for_collision()
                if in_collision:
                    self.active = False
                    # Draw an orange square on the snake's head to indicate where game ending collision occurred.
                    self.make_snake_head_orange()
                    self.display_game_over_message()
                else:
                    if self.is_snake_colliding_with_apple():
                        self.snake.nodes.append(tail_node)
                        self.delete_apple()
                        self.spawn_apple()
        self.master.after(1000 // FRAMES_PER_SECOND, self.move)

def main():
    root = Tk.Tk()
    Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()
