# Genetic Algorithm learning Flappy Bird
This is my implementation of [felschatz Sloppy-Bird repo](https://github.com/felschatz/Sloppy-Block/tree/master).




This  project implements a genetic algorithm to train an MLP to play a Flappy Bird clone. The Flappy bird clone is made using pygame.


### Project Structure

- Main Script: The main script `main.py` initilizes the game, all the birds and pipes, draws the UI, score updating and handles which birds are bred in the next generation.

- Bird Class: The `bird.py` has the Bird class which handles collision detection and genetic algorithm. This class handles feedforward and the implementation of the breeding and mutation

- Pipe Class: The `pipe.py` file defines a class for the pipes that the birds must navigate through. Pipes have coordinate properties that the Bird class use for collision detection and uses it in calculating a parameter in the bird's model


Genetic Algorithm Overview

The genetic algorithm used in this project works as follows:

- Initialization: The algorithm starts by initializing a population of AI agents (birds). Each bird is assigned random weights for its neural network, which determines its behavior.

- Simulation:  Birds attempt to navigate through the pipes using their neural networks to make decisions on whether to jump or not.

- Fitness Evaluation: Birds are rewarded with fitness if they stay alive the longest and go through as many pipes. The highest ever fitness is saved

- Selection: The top 2 fittest birds from the current generation are selected to breed the next generation.

- Crossover and Mutation: The selected birds are bred through crossover, where their genetic material (weights) is combined to create offspring. Mutation might occur adding variance.


- Next Generation: The offspring become the next generation of birds, replacing the previous generation. This process repeats for every generation until a bird is so good it no longer looses.



From my testing the best result I got was upwards of 5000 score by generation 17. I quit before the bird could die

