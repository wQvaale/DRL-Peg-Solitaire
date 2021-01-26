from HexGrid import Triangle
import random

class RandomAgent:

    def getMove(self, board):
        jumper = random.randint(0, board.size*(board.size+1)/2 - 1)
        jumpee = random.randint(0, board.size*(board.size+1)/2 - 1)
        return jumper, jumpee


        