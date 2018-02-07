# ColumbiaX: CSMM.101x - Assigment week 2
# Search algorithms - Josef Sertl

import math

class SwitchDirection:
    UP = 'Up'
    DOWN = 'Down'    
    LEFT = 'Left'
    RIGHT = 'Right'

class Stack: #Last in - first out LIFO
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
     
class Queue: #First in - first out FIFO
    def __init__(self):
        self.items = []
   
    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)       

    def dequeue(self):
        return self.items.pop()
    
    def isElement(self, item):
        return item in self.items
        
    def size(self):
        return len(self.items)
    
class BoardTree:
    def __init__(self, initialBoard, goalBoard):
        self.initialBoard = initialBoard
        self.goalBoard = goalBoard
        self.explored = []
        self.frontierItems = []
    
    def performBFS(self, inputBoard):
        frontier = Queue()        
        frontier.enqueue(inputBoard)
        self.frontierItems.append(inputBoard.items)
        
        while not frontier.isEmpty():
            board = frontier.dequeue()
            board = Board(*board.items)            
            self.explored.append(board)
                        
            if board.isIdentical(self.goalBoard):
                print('BOARD is identical to GOAL')
                return True
            
            neighborBoardList = board.getNeighborBoards()
                            
            for neighbors in neighborBoardList:
                if not neighbors in self.explored and not neighbors.items in self.frontierItems:
                    frontier.enqueue(neighbors)
                    self.frontierItems.append(neighbors.items)
                                
    def printPath(self):
        counter = 0
        for boards in self.explored:
            counter += 1
            boards.printMatrix('Explored ' + str(counter))
        self.goalBoard.printMatrix('Goal')
        
class Board:
    def __init__(self, *args):
        self.items = []    
        for p in args:
            self.items.append(p)
        self.dim = int(math.sqrt(len(self.items)))
            
    def getMatrix(self):
        self.matrix = []       
        row = []
        for i in range (0,len(self.items)):
           row.append(self.items[i])
           if (i + 1) % self.dim == 0:
               self.matrix.append(row)
               row = []           
            
        return self.matrix
    
    def printMatrix(self, header):
        matrix = self.getMatrix()
        if not header is None:
            print(header)
        for row in matrix:
            print(row)           

    def clone(self):
        return Board(*self.items)
    
    def isIdentical(self, boardCompare):
        for i in range(0, len(self.items)):
            if self.items[i] != boardCompare.items[i]:
                return False
        return True
    
    def getNeighborBoards(self):
        loopList = [SwitchDirection.UP, SwitchDirection.DOWN, SwitchDirection.LEFT, SwitchDirection.RIGHT]
        neighborBoardList = []
        for directions in loopList:
            neighbor = self.getNeighborBoard(directions)
            if not neighbor is None:
                neighborBoardList.append(neighbor)
        return neighborBoardList
    
    def getNeighborBoard(self, direction):
        if self.isSwitchZeroPossible(direction) == False:
            return None
        newBoard = self.clone()
        newBoard.switchZero(direction)
        return newBoard
        
    def switchZero(self, direction): #Up, Down, Left, Right UDLR        
        if self.isSwitchZeroPossible(direction) == False:
            return
        
        currentIndexZero = self.items.index(0)
        newIndexZero = self.getNewZeroPositionAfterSwitch(direction)
        newIndexZeroValue = self.items[newIndexZero]
        self.items[newIndexZero] = 0
        self.items[currentIndexZero] = newIndexZeroValue
    
    def getNewZeroPositionAfterSwitch(self, direction): #Up, Down, Left, Right UDLR
        if self.isSwitchZeroPossible(direction) == False:
            return self.items.index(0) #Current position
        currentIndexZero = self.items.index(0)
        if direction == SwitchDirection.UP:
            return currentIndexZero - self.dim
        elif direction == SwitchDirection.DOWN:
            return currentIndexZero + self.dim
        elif direction == SwitchDirection.LEFT:
             return currentIndexZero - 1
        elif direction == SwitchDirection.RIGHT:
             return currentIndexZero + 1
               
    def isSwitchZeroPossible(self, direction): #Up, Down, Left, Right UDLR
        currentIndexZero = self.items.index(0)       
        if direction == SwitchDirection.UP and currentIndexZero > self.dim - 1:
            return True
        elif direction == SwitchDirection.DOWN and currentIndexZero < len(self.items) - self.dim:
             return True
        elif direction == SwitchDirection.LEFT and currentIndexZero % self.dim > 0:
             return True
        elif direction == SwitchDirection.RIGHT and (currentIndexZero + 1) % self.dim > 0:
              return True
        return False        
        
args = (1,2,0,3,4,5,6,7,8)
args = (1,2,5,3,4,0,6,7,8) #example 1

argsGoal = (0,1,2,3,4,5,6,7,8)
board = Board(*args)
boardGoal = Board(*argsGoal)

board.printMatrix('Start')
boardGoal.printMatrix('Goal')

boardTree = BoardTree(board, boardGoal)
boardTree.performBFS(board)
boardTree.printPath()
    


"""  
boardTree = BoardTree(board, boardGoal)
boardTree.performBFS(board)
boardTree.printPath()

neighborBoardList = board.getNeighborBoards()
for neighbors in neighborBoardList:
    neighbors.printMatrix('Neighbor')

boardTree = BoardTree(board, boardGoal)
boardTree.performBFS(board)
boardTree.printPath()


boardTree = BoardTree(board, boardGoal)
#boardTree.performBFS(board)
boardTree.printPath()

   

neighborBoardList = board.getNeighborBoards()
for neighbors in neighborBoardList:
    neighbors.printMatrix('Neighbor')
    
    
newBoard.switchZero(SwitchDirection.DOWN)
print('Down', newBoard.getMatrix())
     
newBoard.switchZero(SwitchDirection.RIGHT)
print('Right', newBoard.getMatrix())

newBoard.switchZero(SwitchDirection.LEFT)
print('Left', newBoard.getMatrix())

newBoard.switchZero(SwitchDirection.UP)
print('Up', newBoard.getMatrix())
"""