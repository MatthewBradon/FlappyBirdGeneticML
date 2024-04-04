import random

class pipe:


	def __init__(self, WIDTH, HEIGHT, distanceToOldPipe):
		top = random.randint(0,HEIGHT-100)
		# We wanna show something on the lower end.
		self.uppery = random.randint(0,HEIGHT-140)
		self.lowery = self.uppery + 120

		
		#randomize distance of pipes so the bird can learn better
		self.x = distanceToOldPipe/4 + WIDTH + random.randint(0,15)

	def moveLeft(self):
		self.x -= 4
