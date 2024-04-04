import numpy as np
import random

class bird:

    def __init__(self, height, male = None, female = None):

        #Bird properties
        self.y = height/2
        self.velocity = 0
        self.distanceBot = 0
        self.distanceTop = 0
        self.distanceX = 0
        self.distanceGround = 0
        self.distanceCeil = 0
        self.fitness = 0
        self.alive = True
        self.color = tuple(random.randint(0, 255) for _ in range(3))
        
        
        if (male == None):
            #easy network
            self.w1 = np.random.normal(0, scale=0.1, size=(5, 3))
            self.w2 = np.random.normal(0, scale=0.1, size=(3, 1))
        elif (female == None):
            self.w1 = male.w1
            self.w2 = male.w2
            self.mutate()
        else: # Two parents - Breed.
            self.w1 = np.random.normal(0, scale=0.1, size=(5, 3))
            self.w2 = np.random.normal(0, scale=0.1, size=(3, 1))
            self.breed(male, female)

    def processBrain(self, pipeUpperY, pipeLowerY, pipeDistance):

        self.distanceTop = pipeUpperY - self.y
        self.distanceBot = pipeLowerY - self.y
        self.distanceX = pipeDistance
        self.fitness += 0.01



    def handleCollision(self, HEIGHT, BLOCKSIZE, pipe):
        #Check if player collided with upper or lower pipe
        #Check if player is within x coordinates of the pipe
        if ( ((pipe.x >= 20) and (pipe.x <= 20+BLOCKSIZE)) or ((pipe.x+20 >= 20) and (pipe.x+20 <= 20+BLOCKSIZE)) ):
            #Player is within y coordinates of the pipe
            if ( (self.alive) and ((self.y <= pipe.uppery) or (self.y+BLOCKSIZE >= pipe.lowery)) ): 
                #alive player hits a pipe
                self.alive = False
                self.fitness -= 1

        #upper/lower bounds handling (did the bird hit the ground/ceil)
        if (self.y + self.velocity > HEIGHT-BLOCKSIZE): #LowerBounds
            self.y = HEIGHT-BLOCKSIZE
            self.alive = False
            self.fitness -= 1
        elif (self.y + self.velocity < 1): #UpperBounds
            self.y = 0
            self.velocity = 0
            self.alive = False
            self.fitness -= 1


    def feedForward(self):

        BIAS = -0.5
        inputs = [self.y, self.distanceBot, self.distanceTop, self.distanceX,
            self.velocity]


        a1 = self.sigmoid(np.dot(inputs, self.w1))
        a2 = self.sigmoid(np.dot(a1, self.w2))


        if (a2+BIAS > 0):
            return True
        else:
            return False


    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def setWeights(self, w1, w2):
        self.w1 = w1
        self.w2 = w2

    def breed(self, male, female):
        self.w1 = (male.w1 + female.w1) / 2
        self.w2 = (male.w2 + female.w2) / 2
        self.mutate()

    def mutate(self):
        for i in range(len(self.w1)):
            for j in range(len(self.w1[i])):
                self.w1[i][j] = self.getMutation(self.w1[i][j])
        for i in range(len(self.w2)):
            for j in range(len(self.w2[i])):
                self.w2[i][j] = self.getMutation(self.w2[i][j])
									 
    def getMutation(self, weight):  
        # Random learning rate between 0.005 and 0.125
        learningRate = random.randint(0,25) * 0.005


        # Randomly choose to add or subtract the learning rate
        randBool1 = bool(random.getrandbits(1))
        randBool2 = bool(random.getrandbits(1))

        multiplier = 0
        if (randBool1 and randBool2):
            multiplier = 1
        elif (not randBool1 and randBool2):
            multiplier = -1

        return weight + (learningRate * multiplier)
