class Individual:
    _chromosome = []
    _fitness = None
    MIN_VAL = -100
    MAX_VAL = 100

    def __init__(self, chromosome_len):
        for(i in range(chromosome_len)):
            _chromosome.append(random.uniform(MIN_VAL, MAX_VAL))

    def get_fitness():
        return _fitness

    def set_fitness(new_fitness):
        fitness = new_fitness

    def get_chromosome():
        return _chromosome.copy()

    def set_chromosome(new_chromosome):
        _chromosome = new_chromosome.copy()

    def copy():
        ret = Individual(chromosome_len)
        ret.set_fitness(_fitness)
        ret.set_chromosome(_chromosome)
        return ret

    def mutate(mutation_rate):
        '''
        If the mutation rate is less than some randomly chosen value, then we 
        choose a random index and reassign it to a random value. This represents
        the chance for a mutation in an offspring
        '''
        if(random.uniform(0,1) > mutation_rate):
            _chromosome[int(random.uniform(0,len(_chromosome)))] = random.uniform(MAX_VAL, MIN_VAL)

class GeneticAlgorithm:
    population = []
    population_size = None
    chromosome_len = None
    generation = None
    best_individual = None
    mutation_rate = 0.8
    
    def __init__(self, size, rate, length):
        # Set class variables
        population_size = size
        mutation_rate = rate
        chromosome_len = length

        # Generate population
        for(i in range(population_size)):
            population.append(Individual(chromosome_len))

    def get_population():
        return population.copy()
    
    def get_best_individual():
        return best_individual.copy()
    
    def set_individual_fitness(index, fitness):
        population[index].set_fitness(fitness)

    def crossover(parent1, parent2):
        '''
        This function generates a new individual by randomly choosing hyperparameters
        from two parents and then mutating randomly
        '''
        child = Individual(chromosome_len)
        chromosome1 = parent1.get_chromosome()
        chromosome2 = parent2.get_chromosome()
        child_chromosome = []

        # Randomly choose hyperparameters from parents
        for(i in range(chromosome_len)):
            if(random.uniform(0,1) > 0.5):
                child_chromosome.append(chromosome1[i])
            else:
                child_chromosome.append(chromosome2[i])

        child.set_chromosome(child_chromosome)

        # Mutate the child
        child.mutate(mutation_rate)

        return child

    def new_generation():

        # Sort the current population by fitness
        sort_by_fitness()

        # Save the best individual
        if(best_individual is None or population[0].getFitness() > best_individual.getFitness()):
            best_individual = population[0].copy()

        # Take the top half of the population to form the new population
        # Note: this can be changed to something else if we think of a better way
        fit_population = population[:population_size/2].copy()

        # Randomly choose parents to crossover for a new generation
        population = []
        for(i in range(population_size)):
            population.append(crossover(fit_population[int(random.uniform(0,len(fit_population)))], fit_population[int(random.uniform(0,len(fit_population)))]))

        generation+=1

    def sort_by_fitness():
        '''
        This function sorts the population by fitness value.

        Note: I just used bubblesort to do this since the population size is 
        not large. If someone else wants to implement a better sort function,
        they are more than welcome to, however I do not think that it will be 
        worth while.
        '''
        for(i in range(chromosome_len-1)):
            for(j in range(chromosome_len-i-1)):
                if(population[j].get_fitness() > population[j+1].get_fitness()):
                    population[j], population[j+1] = population[j+1], population[j]
