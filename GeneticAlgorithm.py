import random


class Individual:

    def __init__(self, chromosome_len):
        self.chromosome_len = chromosome_len
        self._chromosome = []
        self._fitness = -999.01
        self.MIN_VAL = [0, 0, 0, 0, 0, 0]
        self.MAX_VAL = [1.9, 40, 40, 40, 40, 40]
        for i in range(chromosome_len):
            rand_num = random.uniform(self.MIN_VAL[i], self.MAX_VAL[i])
            self._chromosome.append(rand_num)

    def get_fitness(self):
        return self._fitness

    def set_fitness(self, new_fitness):
        self._fitness = new_fitness

    def get_chromosome(self):
        return self._chromosome[:]

    def set_chromosome(self, new_chromosome):
        self._chromosome = new_chromosome[:]

    def copy(self):
        ret = Individual(self.chromosome_len)
        ret.set_fitness(self._fitness)
        ret.set_chromosome(self._chromosome)
        return ret

    def mutate(self, mutation_rate):
        '''
        If the mutation rate is less than some randomly chosen value, then we
        choose a random index and reassign it to a random value. This represents
        the chance for a mutation in an offspring
        '''
        if (random.uniform(0, 1) > mutation_rate):
            randindex = int(random.uniform(0, len(self._chromosome)))
            self._chromosome[randindex] = random.uniform(self.MAX_VAL[randindex], self.MIN_VAL[randindex])


class GeneticAlgorithm:

    def __init__(self, size, rate, length):
        self.population = []
        self.generation = 0
        self.best_individual = None
        # Set class variables
        self.population_size = size
        self.mutation_rate = rate
        self.chromosome_len = length

        # Generate population
        for i in range(self.population_size):
            self.population.append(Individual(self.chromosome_len))

    def get_population(self):
        return self.population[:]

    def set_population(self, new_pop):
        self.population = new_pop.copy()

    def get_best_individual(self):
        return self.best_individual

    def set_individual_fitness(self, index, fitness):
        self.population[index].set_fitness(fitness)

    def crossover(self, parent1, parent2):
        '''
        This function generates a new individual by randomly choosing hyperparameters
        from two parents and then mutating randomly
        '''
        child = Individual(self.chromosome_len)
        chromosome1 = parent1.get_chromosome()
        chromosome2 = parent2.get_chromosome()
        child_chromosome = []

        # Randomly choose hyperparameters from parents
        for i in range(self.chromosome_len):
            if (random.uniform(0, 1) > 0.5):
                child_chromosome.append(chromosome1[i])
            else:
                child_chromosome.append(chromosome2[i])

        child.set_chromosome(child_chromosome)

        # Mutate the child
        child.mutate(self.mutation_rate)

        return child

    def new_generation(self):

        # Sort the current population by fitness
        self.sort_by_fitness()
        print([i.get_fitness() for i in self.population])

        # Save the best individual
        if (self.best_individual is None or self.population[0].get_fitness() > self.best_individual.get_fitness()):
            self.best_individual = self.population[0].copy()

        # Take the top half of the population to form the new population
        # Note: this can be changed to something else if we think of a better way
        # print('pop size',int(self.population_size/2 ))
        # print('pop size float ',self.population_size/2 )
        self.fit_population = self.population[:int(self.population_size / 2)][:]

        # Randomly choose parents to crossover for a new generation
        self.population = [self.best_individual.copy()]
        while len(self.population) < self.population_size:
            self.population.append(self.crossover(self.fit_population[int(random.uniform(0, len(self.fit_population)))],
                                                  self.fit_population[
                                                      int(random.uniform(0, len(self.fit_population)))]))

        self.generation += 1

    def sort_by_fitness(self):
        '''
        This function sorts the population by fitness value.
        Note: I just used bubblesort to do this since the population size is
        not large. If someone else wants to implement a better sort function,
        they are more than welcome to, however I do not think that it will be
        worth while.
        '''
        for i in range(self.population_size - 1):
            for j in range(self.population_size - i - 1):
                if (self.population[j].get_fitness() < self.population[j + 1].get_fitness()):
                    self.population[j], self.population[j + 1] = self.population[j + 1], self.population[j]
