#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Final Project: Game

Snake emulated by Carson Chapman (504670786)
"""

import Tkinter as Tk
import random as rd

# GLOBAL CONSTANTS:
FRAMES_PER_SECOND = 5 # the number of snake updates per second
TILE_WIDTH = 42 # the width of each tile on the game board
X_TILES = 15 # the number of horizontal tiles on the board, not including the border
Y_TILES = 15 # the number of vertical tiles on the board, not including the border
WIDTH = TILE_WIDTH*X_TILES + 2*TILE_WIDTH # the overall width of the game window
HEIGHT = TILE_WIDTH*Y_TILES + 2*TILE_WIDTH # the overall height of the game window
BORDER_COLOR = "black" # the color of the border
BG_COLOR = "white" # the color of where the snake moves around
APPLE_COLOR = "green" # the color of an Apple
SNAKE_COLOR = "red" # the color of the Snake
GAME_OVER_COLOR = "orange" # the color of a SnakeNode that causes gameover

# The class for an Apple object
# It keeps track of the x and y tile position and draws its shape on the canvas
class Apple(object):
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.shape = self.canvas.create_oval(self.x*TILE_WIDTH, self.y*TILE_WIDTH, (self.x+1)*TILE_WIDTH, (self.y+1)*TILE_WIDTH, fill=APPLE_COLOR)

# The class for a SnakeNode object
# SnakeNodes are the segments of the snake which together are the entire snake
# This class keeps track of each node's x and y tile position and draws it on the
# game board
class SnakeNode(object):
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.shape = self.canvas.create_rectangle(self.x*TILE_WIDTH, self.y*TILE_WIDTH, (self.x+1)*TILE_WIDTH, (self.y+1)*TILE_WIDTH, fill=SNAKE_COLOR)

# The class for the snake
# It keeps track of the x and y coordinates of the head and has a list of
# SnakeNodes which it uses to move the snake around the board, as well as
# a current direction that the Snake is travelling in, and its length
class Snake(object):
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.nodes = [ SnakeNode(canvas,x,y) ] # creates a list with only the head
        # dir is the direction:
        # -1 is not moving, 0 is right, 1 is up, 2 is left, 3 is down
        # initialize the Snake as standing still to make it more user friendly
        self.dir = -1
        # set the length of the Snake to 1 to keep track of it without
        # having to repeatedly call len(self.snake.nodes)
        self.length = 1
    
    # returns True if the Snake contains a SnakeNode at the grid position (x,y)
    # otherwise returns False
    def contains(self,x,y):
        for node in self.nodes:
            if node.x == x and node.y == y:
                return True
        return False
    
    # Sets the Snake's direction to dir as long as the Snake's length is 1
    # or if dir is not the direction of the SnakeNode directly behind the head.
    # Direction 0 is right, 1 is up, 2 is left, and 3 is down
    # I will refer to the second node in the list of nodes as the "neck node"
    # since it is directly behind the head.
    def setDir(self,dir):
        # if the snake is length one, change the direction without issue
        # since the head cannot collide with a neck node
        if self.length == 1:
            self.dir = dir
        # if the snake is greater than length one,
        # calculate the tile difference in the x and y direction
        # between the head node and the neck node to make sure
        # that dir is not in the direction of the neck node
        else:
            xDiff = self.nodes[0].x - self.nodes[1].x
            yDiff = self.nodes[0].y - self.nodes[1].y
            # to set the direction to right, the head node can't have an x
            # coordinate that is 1 below the neck node or else it will
            # cause a self collision with the neck node, which is annoying
            # to the player if they hit the wrong button
            if dir == 0 and xDiff != -1:
                self.dir = dir
            # if dir is up and the neck node is not directly above the head,
            # set the direction to up
            elif dir == 1 and yDiff != 1:
                self.dir = dir
            # the next 2 cases are the opposites of the last 2
            elif dir == 2 and xDiff != 1:
                self.dir = dir
            elif dir == 3 and yDiff != -1:
                self.dir = dir
    
class Game(object):
    def __init__(self,master):
        # Boolean value determining if the game is running
        self.active = True
        self.master = master
        # create background
        self.canvas = Tk.Canvas(master, width=WIDTH, height=HEIGHT, bg=BORDER_COLOR)
        # create area for snake
        self.canvas.create_rectangle(TILE_WIDTH, TILE_WIDTH, WIDTH - TILE_WIDTH, HEIGHT - TILE_WIDTH, fill=BG_COLOR)
        # Keyboard input will not work on my computer without the following line of code
        self.canvas.focus_set()
        # Place the Snake at a random tile that is not on the border
        self.snake = Snake(self.canvas,rd.randint(1,X_TILES-2),rd.randint(1,Y_TILES-2))
        # Place an apple at a position that is not in the border or occupied by the snake
        newX = rd.randint(1,X_TILES-2)
        newY = rd.randint(1,Y_TILES-2)
        while newX == self.snake.x and newY == self.snake.y:
            newX = rd.randint(1,X_TILES-2)
            newY = rd.randint(1,Y_TILES-2)
        self.apple = Apple(self.canvas,newX,newY)
        # connect arrow keys to Snake's direction and set any key to reset after game over
        self.canvas.bind("<Right>", lambda event: self.setSnakeDir(0))
        self.canvas.bind("<Up>", lambda event: self.setSnakeDir(1))
        self.canvas.bind("<Left>", lambda event: self.setSnakeDir(2))
        self.canvas.bind("<Down>", lambda event: self.setSnakeDir(3))
        self.canvas.bind("<Key>", self.reset)
        self.canvas.pack()
        # start game loop
        self.move()
    
    # This function is only here to allow the arrow keys to be able to reset the
    # game after a game over.
    def setSnakeDir(self,dir):
        if self.active:
            self.snake.setDir(dir)
        else:
            self.reset()
    
    # Resets the game if and only if it is currently game over
    def reset(self,event=_):
        # if it is game over
        if self.active == False:
            # make the game active again
            self.active = True
            # delete the game over labels
            self.canvas.delete(self.label1)
            self.canvas.delete(self.label2)
            # delete each SnakeNode from the canvas
            for node in self.snake.nodes:
                self.canvas.delete(node.shape)
            # delete the apple from the canvas
            self.canvas.delete(self.apple.shape)
            # create a new Snake head at a random position on the board
            self.snake = Snake(self.canvas,rd.randint(1,X_TILES-2),rd.randint(1,Y_TILES-2))
            # place an apple at a position that is not occupied by the snake
            newX = rd.randint(1,X_TILES-2)
            newY = rd.randint(1,Y_TILES-2)
            while newX == self.snake.x and newY == self.snake.y:
                newX = rd.randint(1,X_TILES-2)
                newY = rd.randint(1,Y_TILES-2)
            self.apple = Apple(self.canvas,newX,newY)
    
    # Moves the snake in the current direction by adding a new node on the front
    # and deleting the tail node
    def move(self):
        # if it is not game over
        if self.active == True:
            currentDir = self.snake.dir
            # if the snake is currently moving
            if currentDir != -1:
                # create a new node in the current direction and check for
                # collision with border or tail at the new position and signal the
                # game to stop after this game tick.
                # The final node in the list (the tail node) must be deleted
                # before the collision check so that the snake does not collide
                # with where the tail node was before the movement. It may need
                # to be readded later if the Snake head hits an apple, so
                # its x and y positions on the game board should be recorded
                tailNode = self.snake.nodes[len(self.snake.nodes)-1]
                tailX = tailNode.x
                tailY = tailNode.y
                self.canvas.delete(tailNode.shape)
                del self.snake.nodes[len(self.snake.nodes)-1]
                if currentDir == 0:
                    a_node = SnakeNode(self.canvas,self.snake.x+1,self.snake.y)
                    self.snake.x = self.snake.x+1
                    if self.snake.x == X_TILES + 1 or self.snake.contains(self.snake.x, self.snake.y):
                        self.active = False
                elif currentDir == 1:
                    a_node = SnakeNode(self.canvas,self.snake.x,self.snake.y-1)
                    self.snake.y = self.snake.y-1
                    if self.snake.y == 0 or self.snake.contains(self.snake.x, self.snake.y):
                        self.active = False
                elif currentDir == 2:
                    a_node = SnakeNode(self.canvas,self.snake.x-1,self.snake.y)
                    self.snake.x = self.snake.x-1
                    if self.snake.x == 0 or self.snake.contains(self.snake.x, self.snake.y):
                        self.active = False
                elif currentDir == 3:
                    a_node = SnakeNode(self.canvas,self.snake.x,self.snake.y+1)
                    self.snake.y = self.snake.y+1
                    if self.snake.y == Y_TILES + 1 or self.snake.contains(self.snake.x, self.snake.y):
                        self.active = False
                # add the new head node to the list
                self.snake.nodes = [ a_node ] + self.snake.nodes
                # check for collision with apple
                if self.snake.x == self.apple.x and self.snake.y == self.apple.y:
                    # if there is a collision, delete the apple and create a new
                    # one that is not on the snake. Then add a new 
                    self.canvas.delete(self.apple.shape)
                    newX = rd.randint(1,X_TILES-2)
                    newY = rd.randint(1,Y_TILES-2)
                    while self.snake.contains(newX,newY):
                        newX = rd.randint(1,X_TILES-2)
                        newY = rd.randint(1,Y_TILES-2)
                    self.apple = Apple(self.canvas, newX, newY)
                    self.snake.length += 1
                    self.snake.nodes = self.snake.nodes + [ SnakeNode(self.canvas,tailX,tailY)]
                # if the snake hit the border or itself,
                # draw the head node in orange to indicate where the game over
                # occured and display the game over message.
                # WARNING: If the game window is not large enough,
                # the game over message will be cut off out of the window.
                if self.active == False:
                    self.canvas.delete(self.snake.nodes[0].shape)
                    self.snake.nodes[0].shape = self.canvas.create_rectangle(self.snake.nodes[0].x*TILE_WIDTH, self.snake.nodes[0].y*TILE_WIDTH, (self.snake.nodes[0].x+1)*TILE_WIDTH, (self.snake.nodes[0].y+1)*TILE_WIDTH, fill=GAME_OVER_COLOR)
                    self.label1 = self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game over! Final length: "+str(self.snake.length))
                    self.label2 = self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 20, text="Press any key to play again!")
            # repeat the game loop after 1000 / FRAMES_PER_SECOND milliseconds
        self.master.after(1000 / FRAMES_PER_SECOND,self.move)

def main():
    root = Tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()
