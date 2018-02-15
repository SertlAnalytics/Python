# ColumbiaX: CSMM.101x - Assigment week 2
# Search algorithms - 2018-02-01
# Copyright Josef Sertl

import math
import time
import os
import psutil
import sys
import ast
import random

class SwitchDirection: #UDLR
    UP = 'Up'
    DOWN = 'Down'    
    LEFT = 'Left'
    RIGHT = 'Right'
    NONE = 'None'   
    
class SwitchDirectionList:
    LIST = [SwitchDirection.UP, SwitchDirection.DOWN, SwitchDirection.LEFT, SwitchDirection.RIGHT]

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
    def __init__(self, initial_board, goal_board):
        self.initial_board = initial_board
        self.goal_board = goal_board
        self.explored = []
        self.frontier_items = []
        self.success_board = None
        self.success_path = []
        self.nodes_expanded = 0
        self.max_search_depth = 0
    
    def performBFS(self, input_board): #QUEUE: FIRST IN FIRST OUT (FIFO)
        frontier = Queue()        
        frontier.enqueue(input_board)
        self.frontier_items.append(input_board.items)
        
        while not frontier.isEmpty():
            board = frontier.dequeue()
            self.explored.append(board)
            
            if board.isIdentical(self.goal_board):
                print('BOARD is identical to GOAL')
                self.success_board = board
                self.success_path = self.get_success_path()
                return True
            
            neighborBoardList = board.getNeighborBoards(False)
            self.nodes_expanded += 1
            if self.nodes_expanded % 10000 == 0:
                print('self.nodes_expanded: {}'.format(self.nodes_expanded))
                
            if self.max_search_depth < board.level_in_searchtree:
                self.max_search_depth = board.level_in_searchtree + 1
                            
            for neighbors in neighborBoardList:               
                if not neighbors in self.explored and not neighbors.items in self.frontier_items:
                    frontier.enqueue(neighbors)
                    self.frontier_items.append(neighbors.items)
   
    def performDFS(self, input_board): #STACK: LAST IN FIRST OUT (LIFO)
        frontier = Stack()        
        frontier.push(input_board)
        self.frontier_items.append(input_board.items)
        
        while not frontier.isEmpty():
            board = frontier.pop()
            self.explored.append(board)
#            direction = board.direction_from_parent
#            items = board.items
            
            if board.isIdentical(self.goal_board):
                print('BOARD is identical to GOAL')
                self.success_board = board
                self.success_path = self.get_success_path()
                return True
            
            neighborBoardList = board.getNeighborBoards(True)
            self.nodes_expanded += 1
            if self.nodes_expanded % 10000 == 0:
                print('self.nodes_expanded: {}'.format(self.nodes_expanded))
            if self.max_search_depth < board.level_in_searchtree:
                self.max_search_depth = board.level_in_searchtree + 1
                            
            for neighbors in neighborBoardList:    
#                direction = neighbors.direction_from_parent
                if not neighbors in self.explored and not neighbors.items in self.frontier_items:
                    frontier.push(neighbors)
                    self.frontier_items.append(neighbors.items)

    def performAST(self, input_board):
        frontier = Queue()        
        frontier.enqueue(input_board)
        self.frontier_items.append(input_board.items)
        
        while not frontier.isEmpty():
            board = frontier.dequeue()
            self.explored.append(board)
            
            if board.isIdentical(self.goal_board):
                print('BOARD is identical to GOAL')
                self.success_board = board
                self.success_path = self.get_success_path()
                return True
            
            neighborBoardList = board.getNeighborBoards()
            self.nodes_expanded += 1
            if self.max_search_depth < board.level_in_searchtree:
                self.max_search_depth = board.level_in_searchtree + 1
                            
            for neighbors in neighborBoardList:               
                if not neighbors in self.explored and not neighbors.items in self.frontier_items:
                    frontier.enqueue(neighbors)
                    self.frontier_items.append(neighbors.items)
                             
    def printPathExplored(self):
        counter = 0
        for boards in self.explored:
            counter += 1
            boards.printMatrix('Explored ' + str(counter))
        self.goalBoard.printMatrix('Goal')
        
    def print_success_path(self):       
        for boards in self.success_path:
            boards.printMatrix('Success path - created by switch: ' + boards.direction_from_parent) 
            
    def get_path_to_goal(self):
        path_to_goal = []        
        for boards in self.success_path:
            if boards.direction_from_parent != SwitchDirection.NONE:
                path_to_goal.append(boards.direction_from_parent)
        return path_to_goal
            
    def get_success_path(self):
        success_path_inverted = []
        success_path_inverted.append(self.success_board)
        parent_board = self.success_board.parent_board
        while not parent_board is None: 
            success_path_inverted.append(parent_board)
            parent_board = parent_board.parent_board
        return success_path_inverted[::-1] #.reverse()
    
class Board_Helper:
    def __init__(self, dim):        
        self.dim = dim
        self.number_mapping = []
        for k in range(1, self.dim + 1):
            for m in range(1, self.dim + 1):
                self.number_mapping.append([k,m])                

    def get_number_misplaced_tiles(self, board):
        counter = 0
        for k in range(0,len(board.items)):
            if board.items[k] != k and k > 0: # 0 is not regarded as wrong
                counter += 1
        return counter
    
    def get_manhattan_distance(self, board):        
        diff = 0
        for k in range(0,len(board.items)):
            value = board.items[k]
            if value > 0: # 0 is not regarded as wrong
                position_k = self.get_manhattan_value(k)
                position_value = self.get_manhattan_value(value)
                diff += abs(position_k[0] - position_value[0]) + abs(position_k[1] - position_value[1])           
        return diff
    
    def get_manhattan_value(self, number):        
        return(self.number_mapping[number]) 
    
    def get_UDLR_list(self, position_zero):
        mapping = self.number_mapping[position_zero]
        udlr = []
        if mapping[0] > 1:
            udlr.append(SwitchDirection.UP)
        if mapping[0] < self.dim:
            udlr.append(SwitchDirection.DOWN)
        if mapping[1] > 1:
            udlr.append(SwitchDirection.LEFT)
        if mapping[1] < self.dim:
            udlr.append(SwitchDirection.RIGHT)
        return udlr
            
    def get_reversed_UDLR_list(self, position_zero):       
        udlr = self.get_UDLR_list(position_zero)
        return udlr[::-1] 
    
    def get_position_zero_after_switch(self, position_zero, switch_direction):
        mapping = self.number_mapping[position_zero].copy() # flat copy
        print(mapping)
        if switch_direction == SwitchDirection.UP:
            mapping[0] = mapping[0] - 1
        elif switch_direction == SwitchDirection.DOWN:
            mapping[0] = mapping[0] + 1
        elif switch_direction == SwitchDirection.LEFT:
            mapping[1] = mapping[1] - 1
        elif switch_direction == SwitchDirection.RIGHT:
            mapping[1] = mapping[1] + 1
        print(mapping)
        return self.number_mapping.index(mapping)
        
class Board:    
    def __init__(self, *args):
        self.items = []    
        for p in args:
            self.items.append(p)
        self.dim = int(math.sqrt(len(self.items)))
        self.level_in_searchtree = 1
        self.parent_board = None
        self.direction_from_parent = SwitchDirection.NONE
             
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
    
    def getNeighborBoards(self, reverse_UDLR):        
        neighborBoardList = []
        if reverse_UDLR:
            direction_list = SwitchDirectionList.LIST[::-1]
        else:
            direction_list = SwitchDirectionList.LIST
            
        for directions in direction_list:
            neighbor = self.getNeighborBoard(directions)
            if not neighbor is None:
                neighborBoardList.append(neighbor)
        return neighborBoardList
    
    def getNeighborBoard(self, direction):
        if self.isSwitchZeroPossible(direction) == False:
            return None
        newBoard = self.clone()
        newBoard.parent_board = self
        newBoard.direction_from_parent = direction
        newBoard.level_in_searchtree = self.level_in_searchtree + 1
        newBoard.switchZero(direction)
#        if not newBoard.parent_board is None:
#            newBoard.parent_board.printMatrix('getNeighborBoard.parent_board')
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
        
class TestBoard:
    def __init__(self, depth_level):
        self.depth_level = depth_level
        self.board = Board(0,1,2,3,4,5,6,7,8)
        self.movements = []
        self.generate_test_board()
        
    def get_test_board_parameters(self):
        return self.board.items
        
    def generate_test_board(self):
        for k in range(0,self.depth_level):
            next_direction = self.get_next_possible_random_switch()
            self.movements.append(next_direction)
            self.board.switchZero(next_direction)
             
    def get_next_possible_random_switch(self):
        next_switch_possible = False
        while not next_switch_possible:
            direction_number = random.randint(1,4) - 1
            direction = SwitchDirectionList.LIST[direction_number]
            next_switch_possible = self.board.isSwitchZeroPossible(direction)
        return direction
    
class Solver:
    def __init__(self, tree_type, *args):
        self.tree_type = tree_type #BFS, DFS, AST
        self.board_start = Board(*args)
        self.board_goal = Board(0,1,2,3,4,5,6,7,8)
        self.board_tree = BoardTree(self.board_start, self.board_goal)
        self.running_start = time.time()
        self.running_end = None
#        self.board_start.printMatrix('board_start')
#        self.board_goal.printMatrix('board_goal')
                     
    def run_algorithm(self):
        if self.tree_type == 'BFS':
            self.board_tree.performBFS(self.board_start)
        elif self.tree_type == 'DFS':
            self.board_tree.performDFS(self.board_start)
        else:
            self.board_tree.performAST(self.board_start)
        self.running_end = time.time()

    def print_success_path(self):
        self.board_tree.print_success_path()
        
    def print_results(self):
#        self.board_tree.print_success_path()
        for entries in self.get_results():
            print(entries)
            
    def write_results(self):        
        with open('output.txt', 'w') as fobj:
            for entries in self.get_results():
               fobj.write(entries + '\n')
        print('Results written to {}'.format(fobj.name) )
     
    def get_results(self):
        value_list = []
        value_list.append('path_to_goal: {}'.format(str(self.board_tree.get_path_to_goal())))
        value_list.append('cost_of_path: {}'.format(len(self.board_tree.success_path)-1))
        value_list.append('notes_expanded: {}'.format(self.board_tree.nodes_expanded))
        value_list.append('search_depth: {}'.format(len(self.board_tree.success_path)-1))
        value_list.append('max_search_depth: {}'.format(self.board_tree.max_search_depth))
        value_list.append('running_time: {0:9.8f}'.format(self.running_end - self.running_start))
        value_list.append('max_ram_usage: {0:9.8f}'.format(self.get_max_ram_usage()/(10**6 * 8)))   
        return value_list
        
    def get_max_ram_usage(self):
        process = psutil.Process(os.getpid())
#        return process.memory_info().rss
        return process.memory_info()[0] # float(2 ** 20)

#board = Board(7,2,4,5,0,6,8,3,1)
board = Board(8,1,2,3,4,5,6,7,0)
board_helper = Board_Helper(3)
print(board_helper.get_number_misplaced_tiles(board))
print(board_helper.number_mapping)
print(board_helper.get_manhattan_distance(board))
print(board_helper.get_UDLR_list(8))
print(board_helper.get_position_zero_after_switch(0, SwitchDirection.DOWN))

print(board_helper.get_position_zero_after_switch(0, SwitchDirection.RIGHT))

#print(board.get_number_misplaced_tiles())
#print(board.get_manhattan_distance())
#type = 'DFS'   
#args = board.items # BFS - 3 levels UDLR

#test = False
#if test:
#    test_board = TestBoard(10)
#    print(tuple(test_board.get_test_board_parameters()))
#    print(test_board.movements)
#    args = tuple(test_board.get_test_board_parameters())
#elif 'python.exe' in sys.executable: #started from command prompt
#    type = sys.argv[1].upper()
#    args = ast.literal_eval(sys.argv[2]) # ast.literal_eval splits the string into a tuple
#else:  
#    type = 'BFS'    
#    args = (1,2,5,3,4,0,6,7,8) # BFS - 3 levels UDLR
#    type = 'DFS'
#
#    
#solver = Solver(type, *args)
#solver.run_algorithm()
#solver.print_results()
#solver.print_success_path()
#solver.write_results()

#args = (3,1,2,6,4,5,0,7,8) # DFS - 3 levels UDLR
#args = (1,4,2,3,7,5,6,0,8) # DFS - 3 levels UDLR
#args = (1,2,0,3,4,5,6,7,8)
#args = (1,2,5,3,4,0,6,7,8) #example 1
#
#args_goal = (0,1,2,3,4,5,6,7,8)
#board_start = Board(*args)
#board_goal = Board(*args_goal)
#
#board_start.printMatrix('Start')
#board_goal.printMatrix('Goal')
#
#board_tree = BoardTree(board_start, board_goal)
#board_tree.performBFS(board_start)
#board_tree.success_board.printMatrix('console: success_board') 
#board_tree.success_board.parent_board.printMatrix('console: success_board.parent_board') 
##boardTree.printPathExplored()
#board_tree.print_success_path()

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