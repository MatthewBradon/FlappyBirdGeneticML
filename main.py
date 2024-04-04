import sys
import copy
import pygame
import numpy as np
import Bird
import Pipe

#Initialize constants
WIDTH = 640 #screensize
HEIGHT = 480 #screensize
BLOCKSIZE = 20 
BIRDS = 90
JUMP_VELOCITY = -13
MAX_FPS = 60
GRAVITY = 1


#pygame initialization
pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

#GlobalVariable Setup
bestInputWeights = [0,0,0,0,0]
bestHiddenWeights = [0,0,0]
player = None
multiPlayer = []
pipes = []
score = 0
running = True
font = pygame.font.SysFont("comicsansms", 72)
littlefont = pygame.font.SysFont("comicsansms", 16)
generation = 1
birdsToBreed = []
highestFitness = 0
highgen = 0
allTimeBestBird = None
maxscore = 0
globalFitness = 0.0
introduceNewGenesFlag = False


def init():

	global player, running, score, multiPlayer, introduceNewGenesFlag

	#Initialize Pipes
	while (len(pipes) > 0): #Kill existing
		pipes.pop(0)
	initPipe()
	initPipe(w = WIDTH + WIDTH/2)

	#Reset some global variables
	score = 0
	running = True


	#This is the first init. New ones, are covered in the else below.
	if (len(birdsToBreed) == 0):
		#Create the first generation of birds
		for _ in range(BIRDS):
			multiPlayer.append(Bird.bird(HEIGHT))

	else:
		#Create the next generation of birds
		multiPlayer = []

		#Add best bird of last generation alive without mutation
		_ = Bird.bird(HEIGHT)
		_.setWeights(birdsToBreed[0].w1,
					birdsToBreed[0].w2)
		multiPlayer.append(_)



		#Add the best of all time alive without mutation
		_ = Bird.bird(HEIGHT)
		_.setWeights(bestInputWeights,
					bestHiddenWeights)
		multiPlayer.append(_)


		#Breed and mutate the last generations 2 best birds sometimes
		for _ in range(int(BIRDS/3)):
			multiPlayer.append(Bird.bird(HEIGHT, birdsToBreed[0], birdsToBreed[1]))


		#Breed and mutate the last generations best bird a couple of times
		for _ in range(int(BIRDS/3)):
			multiPlayer.append(Bird.bird(HEIGHT, birdsToBreed[0]))


		#Add the rest of the birds
		for _ in range(int(BIRDS/3)-2):

			if (introduceNewGenesFlag): #Bad genes - replace some.
				multiPlayer.append(Bird.bird(HEIGHT))
			else:
				#Breed and mutate the last generations second best bird sometimes
				multiPlayer.append(Bird.bird(HEIGHT, birdsToBreed[1]))

		if (introduceNewGenesFlag):
			introduceNewGenesFlag = False

def initPipe(w = WIDTH):
	dist = 0
	for p in pipes:
		dist = p.x
	return pipes.append(Pipe.pipe(w, HEIGHT, dist))

def processPipeMovement(pipes):

	global score, multiPlayer

	for p in pipes:
			#Remove pipe if passed
			if (p.x < -30):
				pipes.pop(0)
				initPipe()
				score += 1 
				for player in multiPlayer: #Reward living birds
					if (player.alive):
						player.fitness += 3

			p.moveLeft() # Move the pipe to the left

def draw(window):
	#Background
	pygame.draw.rect(window, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

	#Pipes
	for p in pipes:
		pygame.draw.rect(window, (255, 0, 0), (p.x, 0, 30, p.uppery))
		pygame.draw.rect(window, (255, 0, 0), (p.x, p.lowery, 30, HEIGHT))


	#Birds
	for player in multiPlayer:
		if (player.alive):
				pygame.draw.rect(window, player.color,
									(20,  player.y, BLOCKSIZE, BLOCKSIZE))
				
def drawScores(alive, score, fitness=None, gen=None, maxscore=None, birdsAliveCount=None):

	if (not alive):
		return
	

	textColor = (255, 255, 255)

	text = font.render("Score {}".format(score), True, textColor)
	window.blit(text,(WIDTH/2 - text.get_width() // 2, 0))

	text = littlefont.render("Fitness {}".format(round(fitness, 2)), True, textColor)
	window.blit(text,(WIDTH - text.get_width() - 30, 0))

	text = littlefont.render("Generation {}".format(gen), True, textColor)
	window.blit(text,(WIDTH - text.get_width() - 30, text.get_height()))

	text = littlefont.render("Best Score {}".format(round(maxscore, 2)), True, textColor)
	window.blit(text,(WIDTH - text.get_width() - 30, text.get_height()*2))

	text = littlefont.render("Birds Alive {}".format(birdsAliveCount), True, textColor)
	window.blit(text,(WIDTH - text.get_width() - 30, text.get_height()*3))

def getAliveBird():
	for player in multiPlayer:
		if (player.alive):
			return player

	return None

def processBirdMovement(player):
			
			global currentfitness, birdsAliveCount, globalFitness

			#Ignore dead birds
			if(not player.alive):
				return

			#Gravity
			player.velocity += GRAVITY
			
			#Check bird collision
			player.handleCollision(HEIGHT, BLOCKSIZE, p)
			
			
			if (player.alive):
				player.y += player.velocity
				birdsAliveCount += 1
		
			#Update what the bird sees to make decisions
			player.processBrain(p.uppery, p.lowery, p.x)
			currentfitness = player.fitness
			globalFitness = player.fitness

			
			if ( player.feedForward() ):
				player.velocity = JUMP_VELOCITY

def createNextGeneration():

	global multiPlayer, birdsToBreed, highestFitness, highgen, allTimeBestBird, bestInputWeights, bestHiddenWeights, maxscore, generation, introduceNewGenesFlag, score

	birdsToBreed = []

	#Find the 2 best birds of last generation
	for birdIndex in range(2): 

		bestBird = -1
		bestFitness = -10

		#Find the best bird in multiPlayer
		for i in range(len(multiPlayer)): 
			player = multiPlayer[i]
			if (player.fitness > bestFitness):

				bestFitness = player.fitness
				bestBird = i

				if (bestFitness >= highestFitness):
					highestFitness = bestFitness


		#If the best bird is the best bird of all time save its stats
		if ( (birdIndex == 1) and (bestFitness >= highestFitness) ):
			
			allTimeBestBird = multiPlayer[bestBird]
			bestInputWeights =  copy.deepcopy(
								multiPlayer[bestBird].w1)
			bestHiddenWeights =  copy.deepcopy(
								multiPlayer[bestBird].w2)
			highestFitness = bestFitness
			highgen = generation
			maxscore = score

		#store the (two) best birds in the breeding list
		birdsToBreed.append(copy.deepcopy(multiPlayer[bestBird]))
		multiPlayer.pop(i)

	
		#If no progress was made in the last 50 generations - new genes.
		if (generation-highgen > 50):
			introduceNewGenesFlag = True

#First init
init()

#The game
while True:
	draw(window) 
	currentfitness = 0.0

	if (running):

		processPipeMovement(pipes)

		birdsAliveCount = 0

		#Get closest pipe
		p = pipes[0] 

		#Update all birds
		for player in multiPlayer:
			processBirdMovement(player)

		#Check if all birds are dead
		if (birdsAliveCount == 0):
			running = False

		#Draw score and information
		drawScores(alive=True, fitness=currentfitness, gen=generation, score=score, maxscore=maxscore, birdsAliveCount=birdsAliveCount)

	elif ( (score > 0) or (maxscore > 0) or (globalFitness > 0.2) ):#Birds are dead

		#Only if atleast one bird made it through one pipe
		createNextGeneration()

		generation += 1

		init()

	#Update the screen
	pygame.display.update()
	fps.tick(MAX_FPS)
