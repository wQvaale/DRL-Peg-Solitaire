from HexGrid import Triangle

class SimWorld:

    def __init__(self, shape="Triangle", size=4, holes=[(0,0)]):
        if shape == "Triangle":
            self.board = Triangle(size, holes)

    def are_there_legal_moves(self):
        for hole in self.board.holes:
            for jumpee in hole.neighbours:
                for jumper in jumpee.neighbours:
                    y = jumper.y - jumpee.y
                    x = jumper.x - jumpee.x
                    if hole.y == jumpee.y - y and hole.x == jumpee.x - x:
                        #if hole empty, perform jump
                        if hole.empty and not jumper.empty and not jumpee.empty:
                            return True
        return False
             

    def is_victory(self):
        num_cells = self.board.size*(self.board.size+1)/2
        if len(self.board.holes) == num_cells - 1:
            return True
    
    def solitaire_jump(self, jumper, jumpee):
        #not sure how this will interact with the rest of the system but it is something
            #check if neighbours
            if jumper in jumpee.neighbours:
                #calculate hole
                y = jumper.y - jumpee.y
                x = jumper.x - jumpee.x
                #if calculated hole exists
                if 0 <= jumpee.y - y <= self.board.size and 0 <= jumpee.x - x <= self.board.size:
                    hole = self.board.grid[jumpee.y - y][ jumpee.x - x]
                    #if hole empty, perform jump
                    if hole.empty and not jumper.empty and not jumpee.empty:
                        jumper.empty = True
                        jumpee.empty = True
                        hole.empty = False
                        self.board.holes.remove(hole)
                        self.board.holes.append(jumper)
                        self.board.holes.append(jumpee)
                        print(jumper, " jumped over ", jumpee, " to ", hole)
                    else:
                        print("not legal")
                else:
                    print("not legal")
            else:
                print("not legal")

    def play_solitaire_human_terminal(self):
        self.board.vis()
        while True:
         
            inp = input("move")
            jumper = inp[0]
            jumpee = inp[1]

            for row in range(len(self.board.grid)):
                for col in range(row+1):
                    print(self.board.grid[row][col].cell_id)
                    if self.board.grid[row][col].cell_id == jumper:
                        jumper = self.board.grid[row][col]
                    if self.board.grid[row][col].cell_id == jumpee:
                        jumpee = self.board.grid[row][col]
            self.solitaire_jump(jumper, jumpee)
            self.board.vis()
            
            if self.is_victory():
                print("congrats")
                break
            elif not self.are_there_legal_moves():
                print("u suck")
                break
    
    

s = SimWorld()
s.play_solitaire_human_terminal()