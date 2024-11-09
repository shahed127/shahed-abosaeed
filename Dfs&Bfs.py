from copy import deepcopy
from collections import deque 

directions=["up","left","down","right"]

class Square:
    def __init__(self,x,y,type) -> None:
        self.x= x
        self.x= y
        self.type= type

    def __str__(self)-> str:
        if self.type == "blanc":
         return "-"
        elif self.type == "white":
           return "0"
        elif self.type == "red_magnet":
           return "R"
        elif self.type == "purple_magnet":
           return "P"
        elif self.type == "black":
           return "*"
          
class Magnets:
    def __init__(self,board,white_cells) -> None:
        self.board = board
        self.white_cells = white_cells

    def getPosition(self , magnet_type)->None:
        for row in self.board:
            for square in row:
                if square.type == magnet_type:
                    return square.x , square.y
                
    def is_white_cell(self, x, y):
        return (x, y) in self.white_cells
                
    def attract(self,t_x,t_y):
        rows=len(self.board)
        columns=len(self.board[0])
        for y in range(columns):
            if y != t_y and self.board[t_x][y].type in ["black", "purple_magnet"]:
                direction = -1 if y > t_y else 1
                new_y = y + direction
                if self.board[t_x][new_y].type in ["blanc", "white"]:
                    self.board[t_x][new_y].type = self.board[t_x][y].type
                    self.board[t_x][y].type = "white" if self.is_white_cell(t_x, y) else "blanc"


        for x in range(rows):
            if x != t_x and self.board[x][t_y].type in ["black", "purple_magnet"]:
                direction = -1 if x > t_x else 1
                new_x = x + direction
                if self.board[new_x][t_y].type in ["blanc", "white"]:
                    self.board[new_x][t_y].type = self.board[x][t_y].type
                    self.board[x][t_y].type = "white" if self.is_white_cell(x, t_y) else "blanc"


    def repel(self,t_x,t_y):
        rows=len(self.board)
        columns=len(self.board[0])
        for y in range(columns):
            if y != t_y and self.board[t_x][y].type in ["black", "red_magnet"]:
                direction = 1 if y > t_y else -1
                new_y = y + direction
                if 0 <= new_y < columns and self.board[t_x][new_y].type in ["blanc", "white"]:
                    self.board[t_x][new_y].type =  self.board[t_x][y].type
                    self.board[t_x][y].type = "white" if self.is_white_cell(t_x, y) else "blanc"

        for x in range(rows):
            if x != t_x and self.board[x][t_y].type in ["black", "red_magnet"]:
                direction = 1 if x > t_x else -1
                new_x = x + direction
                if 0 <= new_x < rows and self.board[new_x][t_y].type in ["blanc", "white"]:
                    self.board[new_x][t_y].type =  self.board[x][t_y].type
                    self.board[x][t_y].type = "white" if self.is_white_cell(x, t_y) else "blanc"

                
        
class State:
    def __init__(self,rows,columns,board,white_cells) -> None:
      self.rows = rows
      self.columns = columns
      self.board = board
      self.white_cells = white_cells
    
    def __str__(self) -> str:
            result=''
            for row in self.board:
                for square in row:
                    result+= str(square)
                result+= '\n'
            return result
    
    def getChildren(self):
        children=[]
        for x in range(self.rows):
           for y in range(self.columns):
               if self.board[x][y].type in ["red_magnet","purple_magnet"]:
                   for direction in directions:
                        new_state=deepcopy(self)
                        new_x,new_y=x,y
                        if direction == "up":
                           new_x-=1
                        elif direction == "down":
                           new_x+=1
                        elif direction == "left":
                           new_y-=1
                        elif direction == "right":
                            new_y+=1
                        if 0<=new_x<self.rows and 0<=new_y<self.columns:
                                
                            if new_state.board[new_x][new_y].type in ["blanc","white"]:
                                new_state.board[new_x][new_y].type=new_state.board[x][y].type
                                new_state.board[x][y].type= "white" if (x,y) in self.white_cells else "blanc"
                              # print(new_state)
                                magnets = Magnets(new_state.board, new_state.white_cells)
                                if new_state.board[new_x][new_y].type == "red_magnet":
                                    magnets.attract(new_x, new_y)
                                elif new_state.board[new_x][new_y].type == "purple_magnet":
                                    magnets.repel(new_x, new_y)
                                children.append(new_state)
        return children
    
    def is_goal(self):
        print(self)
        for row in self.board:
            for square in row:
                if square.type == "white":
                    return False
        return True            
        
                
class Game:
    def __init__(self, initialState) -> None:
        self.initialState = initialState
        self.magnets = Magnets(initialState.board, initialState.white_cells)
        self.currentState=deepcopy(initialState)
        self.visited = set() 
        self.stack=[] 
        self.stack.append(initialState)
        self.queue = deque([initialState]) 

       
    def dfs(self):
        while self.stack:
            current_state=self.stack.pop()
            if current_state.is_goal():
                print("this is the win state")
                print(current_state)
                return  True
            str_current_state = str(current_state)
            print(current_state)
            self.visited.add(str_current_state)
            for child in current_state.getChildren():
                if str(child) not in self.visited:
                    self.visited.add(str(child))
                    self.stack.append(child)
                    #print(child)
        print("no solution")
        return False
    
    def bfs(self):
        while self.queue:
            current_state = self.queue.popleft()  
            if current_state.is_goal():
                print("this is the win state")
                print(current_state)
                return True
            str_current_state = str(current_state)
            print(current_state)
            self.visited.add(str_current_state)
            for child in current_state.getChildren():
                if str(child) not in self.visited:
                    self.visited.add(str(child))
                    self.queue.append(child)
                    #print(child)
        print("No solution ")
        return False

    




    def move(self, magnet_type,t_x,t_y):
        rows=len(self.magnets.board)
        columns=len(self.magnets.board[0])
        #print(rows,columns)
        posision = self.magnets.getPosition(magnet_type)
        if posision:
            current_x,current_y = posision
           # previous_type = self.magnets.board[current_x][current_y].type
            if rows > t_x >=0 and columns > t_y >= 0 and self.magnets.board[t_x][t_y].type in ["blanc","white"]:
                #test= True if self.magnets.board[t_x][t_y].type == "white" else False
                # previous_type = "white" if self.magnets.board[current_x][current_y].type == "white" else "blanc"
                self.magnets.board[t_x][t_y].type= self.magnets.board[current_x][current_y].type
                #self.magnets.board[t_x][t_y].type = magnet_type[0].upper()
                self.magnets.board[current_x][current_y].type = "white" if self.magnets.is_white_cell(current_x, current_y) else "blanc"
                # if test == True:
                #     previous_type = "white"
                if magnet_type=="red_magnet":
                    self.magnets.attract(t_x , t_y )
                if magnet_type == "purple_magnet":
                    self.magnets.repel(t_x,t_y)
                print(self.initialState)
                
            
            else:
                print("target position is not empty")
        else:
            print("magnet's type not found in the board ")


    def createExestBoard():
        print("Enter the cells of the square board:")
        board = [["-","-","0","-"],
                 ["0","-","P","0"],
                 ["-","R","*","-"],
                 ["-","-","0","*"]

        ]
        white_cells = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == '-':
                    sq_type = 'blanc'
                elif board[i][j] == '0':
                    sq_type = 'white'
                    white_cells.append((i, j))
                elif board[i][j]== '*':
                    sq_type = 'black'
                elif board[i][j] == 'R':
                    sq_type = 'red_magnet'
                elif board[i][j] == 'P':
                    sq_type = 'purple_magnet'
                board[i][j]= Square(i, j, sq_type)  
        return board, white_cells


    def createBoard(size):
        print("Enter the cells of the square board:")
        board = []
        white_cells = []
        for i in range(size):
            row = []
            row_input = input(f"Row {i + 1}: ")
            for j, cell in enumerate(row_input):
                if cell == '-':
                    sq_type = 'blanc'
                elif cell == '0':
                    sq_type = 'white'
                    white_cells.append((i, j))
                elif cell == '*':
                    sq_type = 'black'
                elif cell == 'R':
                    sq_type = 'red_magnet'
                elif cell == 'P':
                    sq_type = 'purple_magnet'
                else:
                    print(f"Invalid character '{cell}' at ({i}, {j}). Defaulting to blanc.")
                    sq_type = 'blanc'
                row.append(Square(i, j, sq_type))
            board.append(row)  
        return board, white_cells

                
def main():
    boardEnteringType= input("enter the type of entering:  ' user ' to enter the board row by row , 'initial' to enter an exest board  :")
    if boardEnteringType == "user":
        size = int(input("Enter the size of the square board (e.g., 4 for a 4x4 grid): "))
        board, white_cells = Game.createBoard(size)
    elif boardEnteringType == "initial":
        board, white_cells = Game.createExestBoard()
        size=4
    # white=False
    # white1=False
    new_state = State(size, size, board, white_cells)
    print("Initial Board Configuration:")
    print(new_state)
    game = Game(new_state)
    playType=input("if you want to solve it enter 'alon' , to let the program solve it enter 'solve it' ")
    if playType=="solve it":
        game.bfs()
    elif playType=="alon":
        while True:
            magnet_type = input("Enter magnet type to move (R for Red, P for Purple, Q to quit): ")
            if magnet_type == 'Q':
                break
            elif magnet_type not in ['R', 'P']:
                print("Invalid magnet type. Try again.")
                continue

            try:
                target_x = int(input("Enter target x position: "))
                target_y = int(input("Enter target y position: "))
            except ValueError:
                print("Invalid input. Please enter valid integers for positions.")
                continue

            game.move('red_magnet' if magnet_type == 'R' else 'purple_magnet', target_x, target_y)
            win=0
            for row in board:
                for square in row:
                    if square.type == "white":
                        win+=1
            if win ==0:
                print( "congrats u win ! ")
                break        




if __name__ == '__main__':
    main()


  