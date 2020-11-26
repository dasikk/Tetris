# Tetris - DYOA Advanced at TU Graz WS 2020
# Name:       Dasik Kyryll
# Student ID: 11917139

import pygame, sys, time, random
from pygame.locals import *
from framework import BaseGame


# Recommended Start: init function of Block Class
class Block:
    blocknames = ['clevelandZ', 'rhodeIslandZ', 'blueRicky', 'smashBoy', 'orangeRicky', 'teewee', 'hero']

    def __init__(self, game, block_name):
        self.name = block_name
        self.rotation = random.randint(0, len(game.block_list[block_name]) - 1)
        self.shape = 0
        self.width = 0
        self.height = 0
        self.set_shape(game.block_list[self.name][self.rotation])
        self.x = int(game.board_width / 2) - int(self.width / 2)
        self.y = 0
        self.color = game.block_colors[self.name]

    def set_shape(self, shape):
        self.shape = shape
        self.width = len(shape[0])
        self.height = len(shape)
    pass

    def right_rotation(self, rotation_options):
        if (self.rotation + 1) <= len(rotation_options) - 1:
            self.rotation += 1
            self.set_shape(rotation_options[self.rotation])
        else:
            self.rotation = 0
            self.set_shape(rotation_options[self.rotation])
    pass

    def left_rotation(self, rotation_options):
        if (self.rotation - 1) >= 0:
            self.rotation -= 1
            self.set_shape(rotation_options[self.rotation])

        else:
            self.rotation = len(rotation_options) - 1
            self.set_shape(rotation_options[self.rotation])
        pass

    def x_moves(self, direction):
        if direction == 1:
            self.x += 1
        else:
            self.x += -1

    pass

    def y_moves(self):
        if (self.y + self.height) < BaseGame().board_height:
            self.y += 1

    pass


class Game(BaseGame):
    def __init__(self):
        BaseGame.__init__(self)
        self.score = 0
        self.speed = 5
        self.score_dictionary = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }
        self.board = self.get_empty_board()
        self.level = 0

    def run_game(self):
        fall_time = time.time()

        current_block = self.get_new_block()
        next_block = self.get_new_block()

        # GameLoop
        while True:
            self.test_quit_game()
            # TODO Game Logic: implement key events & move blocks (Hint: check if move is valid/block is on the Board)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.is_block_on_valid_position(current_block, -1, 0):
                            Block.x_moves(current_block, -1)
                    if event.key == pygame.K_RIGHT:
                        if self.is_block_on_valid_position(current_block, 1, 0):
                            Block.x_moves(current_block, 1)
                    if event.key == pygame.K_q:
                        if self.ready_for_left_rotation(current_block):
                            Block.left_rotation(current_block, self.block_list[current_block.name])
                    if event.key == pygame.K_e:
                        if self.ready_for_right_rotation(current_block):
                            Block.right_rotation(current_block, self.block_list[current_block.name])
                    if event.key == pygame.K_p:
                        pass
                    if event.key == pygame.K_DOWN:
                        self.speed = self.speed + 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.speed = self.speed - 5

            if not self.is_block_on_valid_position(current_block, 0, 1):
                self.add_block_to_board(current_block)
                current_block = next_block
                next_block = self.get_new_block()

            if not self.is_block_on_valid_position(current_block, 0, 0):
                return 0

            self.remove_complete_line()
            Block.y_moves(current_block)
            # Draw after game logic
            self.display.fill(self.background)
            self.draw_game_board()
            self.draw_score()
            self.draw_level()
            self.draw_next_block(next_block)
            if current_block is not None:
                self.draw_block(current_block)
            pygame.display.update()
            self.set_game_speed(self.speed)
            self.clock.tick(self.speed)

    def ready_for_right_rotation(self, block):
        if (block.rotation - 1) >= 0:
            block_shape = self.block_list[block.name][block.rotation - 1]
        else:
            block_shape = self.block_list[block.name][- 1]
        if (block.x + len(block_shape[0])) > BaseGame().board_width or (
            block.y + len(block_shape)) > BaseGame().board_height:
            return False
        for y in range(len(block_shape)):
            for x in range(len(block_shape[0])):
                if block_shape[y][x] != '.':
                    if self.gameboard[block.y + y][block.x + x] != self.blank_color:
                        return False
        return True
    pass

    def ready_for_left_rotation(self, block):
        if (block.rotation + 1) <= len(self.block_list[block.name]) - 1:
            block_shape = self.block_list[block.name][block.rotation + 1]
        else:
            block_shape = self.block_list[block.name][0]
        if (block.x + len(block_shape[0])) > BaseGame().board_width or (
            block.y + len(block_shape)) > BaseGame().board_height:
            return False
        for y in range(len(block_shape)):
            for x in range(len(block_shape[0])):
                if block_shape[y][x] != '.':
                    if self.gameboard[block.y + y][block.x + x] != self.blank_color:
                        return False
        return True
    pass

    # Check if Coordinate given is on board (returns True/False)
    def is_coordinate_on_board(self, x, y):
        # TODO check if coordinate is on playingboard (in boundary of self.boardWidth and self.boardHeight)
        if x in range(self.board_width):
            if y in range(self.board_height):
                return True
        return False

    # Parameters block, x_change (any movement done in X direction), yChange (movement in Y direction)
    # Returns True if no part of the block is outside the Board or collides with another Block
    def is_block_on_valid_position(self, block, x_change=0, y_change=0):
        # TODO check if block is on valid position after change in x or y direction
        if x_change == 1 or x_change == -1:
            if (block.x + block.width + x_change) > self.board_width or block.x + x_change < 0:
                return False

            for y in range(block.height):
                for x in range(block.width):
                    if block.shape[y][x] != '.':
                        if self.gameboard[block.y + y][block.x + x + x_change] != self.blank_color:
                            return False
                    pass
            return True
        elif y_change == 1:
            if (block.y + block.height) == 18:
                return False
            for y in range(block.height):
                for x in range(block.width):
                    if block.shape[y][x] != '.':
                        if self.gameboard[block.y + y + 1][block.x + x] != self.blank_color:
                            return False
            return True
        elif x_change == 0 and y_change == 0:
            for y in range(block.height):
                for x in range(block.width):
                    if block.shape[y][x] != '.':
                        if self.gameboard[block.y + y][block.x + x] != self.blank_color:
                            return False
            return True
        pass

    # Check if the line on y Coordinate is complete
    # Returns True if the line is complete
    def check_line_complete(self, y_coord):
        # TODO check if line on yCoord is complete and can be removed
        for x in range(self.board_width):
            if self.gameboard[y_coord][x] == self.blank_color:
                return False
        return True

    # Go over all lines and remove those, which are complete
    # Returns Number of complete lines removed
    def remove_complete_line(self):
        # TODO go over all lines and check if one can be removed
        completed_lines = [0] * self.board_height
        lines_removed = 0
        found_empty_line = 0
        found_second_empty_line = 0
        for y in range(self.board_height):
            if self.check_line_complete(y):
                completed_lines[y] = 1
                for x in range(self.board_width):
                    self.gameboard[y][x] = self.blank_color
                lines_removed += 1
        for y in range(self.board_height - 1, 1, -1):
            if completed_lines[y] == 1:
                found_empty_line = 1
            if found_empty_line:
                for h in range(y, 1, -1):
                    for x in range(self.board_width):
                        self.gameboard[y][x] = self.gameboard[y - 1][x]
        for y in range(self.board_height - 1, 1, -1):
            if completed_lines[y - 1] == 1:
                found_second_empty_line = 1
            if found_second_empty_line:
                for h in range(y, 1, -1):
                    for x in range(self.board_width):
                        self.gameboard[y][x] = self.gameboard[y - 1][x]
        if lines_removed:
            self.calculate_new_score(lines_removed, self.level)
            self.calculate_new_level(self.score)
        return lines_removed

    # Create a new random block
    # Returns the newly created Block Class
    def get_new_block(self):
        blockname = random.choice(Block.blocknames)
        block = Block(self, blockname)
        return block

    def add_block_to_board(self, block):
        # TODO once block is not falling, place it on the gameboard
        #  add Block to the designated Location on the board once it stopped moving DONE
        for x in range(block.width):
            for y in range(block.height):
                if block.shape[y][x] != '.':
                    self.gameboard[block.y + y][block.x + x] = block.color
        pass

    # calculate new Score after a line has been removed
    def calculate_new_score(self, lines_removed, level):
        # TODO calculate new score
        # Points gained: Points per line removed at once times the level modifier!
        # Points per lines removed corresponds to the score_directory
        # The level modifier is 1 higher than the current level.
        self.score = self.score + self.score_dictionary[lines_removed] * (level + 1)
        pass

    # calculate new Level after the score has changed
    # TODO calculate new level
    def calculate_new_level(self, score):
        # The level generally corresponds to the score divided by 300 points.
        # 300 -> level 1; 600 -> level 2; 900 -> level 3
        # TODO increase gamespeed by 1 on level up only
        old_level = self.level
        for x in range(0, 30):
            if score >= 300 * x:
                self.level = x
        if self.level > old_level:
            self.speed = self.speed + 1
        pass

    # set the current game speed
    def set_game_speed(self, speed):
        # TODO set the correct game speed!
        # It starts as defined in base.py and should increase by 1 after a level up.
        self.speed = speed
        pass


# -------------------------------------------------------------------------------------
# Do not modify the code below, your implementation should be done above
# -------------------------------------------------------------------------------------
def main():
    pygame.init()
    game = Game()

    game.display = pygame.display.set_mode((game.window_width, game.window_height))
    game.clock = pygame.time.Clock()
    pygame.display.set_caption('Tetris')

    game.show_text('Tetris')

    game.run_game()
    game.show_text('Game Over')


if __name__ == '__main__':
    main()
