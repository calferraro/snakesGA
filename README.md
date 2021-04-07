# snakesGA
A coppeliaSim simulation that learns the optimal hyperparameters for snake motion by using a Genetic Algorithm

## Usage of GeneticAlgorithjm.py
To initialize the algorithm create a new GeneticAlgorithm object from the python class. This automatically creates a population for you and populates it.

Use get_population() to get an array containing all of the individuals in the current generation.

For each individual you can use the get_chromosome() function to get the array containing the hyperparameters. The order of them does not matter, because when they are first created, they are justinitialized to random values, however each time you extract the hyperparameters, you must extract them in the same order to make sure that they are consistent.

After the individual is done executing, you can save its fitness value by using the set_fitness() function and passing the index of the individual from the population and its fitness as parameters.

After this has been done for each individual in the population, call the new_generation function and a new generation will be formed. 

When you have gone through enough generations, you can call the get_best_individual() function to get the best individual. This is the best individual over all generations, not just the last one.

## Definitions of terms

Population - a group of individuals implemented by an array
Chromosome - an array of hyperparameters taht defines an individual
Fitness - a value that represents how well an individual executes the task
Generation - an iteration of the algorithm made up by a population of individuals
Mutation - a random change to an individuals chromosome
Crossover - a combination of two parents to form a child
