# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:59:09 2018

@author: josef sertl
"""

#import numpy as np
import math

class NPuzzle:

    def __init__(self, type, *inputValues):
       self.inputValues = str(inputValues)
       self.type = type
       self.state = []
       if not inputValues is None:
           self.initStateListByInputValues()
           self.initNumberVaribles()
      
    def initStateListByInputValues(self):       
       for n in self.inputValues: 
           self.state.append(n) 
           
    def getZeroPosition(self):
       return self.state.index(0) + 1      
       
    def initNumberVaribles(self):  
       self.zeroPosition = self.getZeroPosition()
       print('self.zeroPosition', self.zeroPosition)
       self.len = len(self.state)
       self.dim = int(math.sqrt(self.len))
       self.zeroRow = int((self.zeroPosition - 1) / self.dim) + 1
       self.zeroColumn = ((self.zeroPosition - 1) % self.dim) + 1
    
    def getClone( self ):  
        clone = NPuzzle(self.type, None)
        for n in self.state:
            clone.state.append(n)
        self.initNumberVaribles()
        return clone
            
    def getElementByPosition( self, n ):
        print(n)
        print(self.state)
        return self.state[n-1]
    
    def isIdenticalWith( self, compareNPuzzle ):
        for n in range(0,self.len-1):
            if self.getElementByPosition(n) != compareNPuzzle.getElementByPosition(n):
                return False            
        return True
    
    def getNeighbors(self):
        self.initNeighbors()
        neighbors = []
        if not self.LeftNeighbor is None:
            neighbors.append(self.LeftNeighbor)
        if not self.RightNeighbor is None:
            neighbors.append(self.RightNeighbor)
        if not self.TopNeighbor is None:
            neighbors.append(self.TopNeighbor)
        if not self.BottomNeighbor is None:
            neighbors.append(self.BottomNeighbor)
        return neighbors
    
    def initNeighbors( self ):
        self.LeftNeighbor = None
        self.RightNeighbor = None
        self.TopNeighbor = None
        self.BottomNeighbor = None
        
        if self.zeroColumn > 1:
            self.LeftNeighbor = self.getClone()
            self.LeftNeighbor.switchElements(self.zeroPosition,'left')
        if self.zeroColumn < 3:
            self.RightNeighbor = self.getClone()
            self.RightNeighbor.switchElements(self.zeroPosition,'right')
        if self.zeroRow > 1:
            self.TopNeighbor = self.getClone()
            self.TopNeighbor.switchElements(self.zeroPosition,'down')
        if self.zeroRow < 3:
            self.BottomNeighbor = self.getClone()
            self.BottomNeighbor.switchElements(self.zeroPosition,'up')
          
    def switchElements(self, n, direction):        
        if direction == 'left':
            newZeroPosition = n - 1            
        elif direction == 'right':
            newZeroPosition = n + 1            
        elif direction == 'up':
            newZeroPosition = n - self.dim            
        else: # down
            newZeroPosition = n + self.dim           
            
        oldValue = self.getElementByPosition(newZeroPosition)
        self.state[newZeroPosition] = 0
        self.state[n] = oldValue
'''       
    def breadthFirstSearch(self, goalTest):
        goalState = New NPuzzle(self.type, goalTest)
'''     
"""
see: https://docs.python.org/3/tutorial/datastructures.html for queues and stacks.
function BREADTH-FIRST-SEARCH(initialState, goalTest)
    returns SUCCESS or FAILURE
    
    frontier = Queue.new(intialState)
    explored = Set.new()
    
    while not frontier.isEmpty():
        state = frontier.dequeue()
        explored.add(state)
        
        if goalTest(state):
            return SUCCESS(state)
            
        for neighbor in state.neighbors():
            if neighbor not in frontier and not explored:
                frontier.enqueue(neighbor)
                
        return FAILURE
"""

"""
>>> from collections import deque
>>> queue = deque(["Eric", "John", "Michael"])
>>> queue.append("Terry")           # Terry arrives
>>> queue.append("Graham")          # Graham arrives
>>> queue.popleft()                 # The first to arrive now leaves
'Eric'
>>> queue.popleft()                 # The second to arrive now leaves
'John'
>>> queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])
"""
z = NPuzzle('bfs', 0,1,2,3,4,5,6,7,8)
y = NPuzzle('bfs', 5,1,2,3,4,0,6,7,8)
#print(z.isIdenticalWith(y))
neighbors = y.getNeighbors()
for n in neighbors:
    print(n.state)
