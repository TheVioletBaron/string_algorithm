import sys, random, string, math

TARGET = "I think this is a reasonable medium sized string!!"

def main(argv):
	#Setup
	population = []
	try:
		population_size = int(sys.argv[1])
		selection = sys.argv[2]
		pC = float(sys.argv[3])
		pM = float(sys.argv[4])
		generations = int(sys.argv[5])
		disInterval = int(sys.argv[6])
	except:
		argumentError()
	
	#create the population
	chars = string.ascii_letters + string.digits + string.punctuation + " "
	for individual in range(population_size):
		populate(population, chars, len(TARGET))

	#train the algorithm
	if selection == "ts":
		for generation in range(generations):
			checkData(population, generation, disInterval)		
			new_population = []
			while len(new_population) < len(population):
				m, f = tournamentSelect(population)
				if random.random() > pC:
					new_population.append(mutate(chars, m, pM))
					new_population.append(mutate(chars, f, pM))
				else:
					new_population.append(mutate(chars, crossover(m, f), pM))
					new_population.append(mutate(chars, crossover(m, f), pM))
			population = new_population

	elif selection == "rs" :
		for generation in range(generations):
			checkData(population, generation, disInterval)
			population.sort(key=fitness)
			new_population = []
			while len(new_population) < len(population):
				m = rankSelect(population)
				f = rankSelect(population)
				if random.random() > pC:
					new_population.append(mutate(chars, m, pM))
					new_population.append(mutate(chars, f, pM))
				else:
					new_population.append(mutate(chars, crossover(m, f), pM))
					new_population.append(mutate(chars, crossover(m, f), pM))
			population = new_population					

	elif selection == "bs" :
		for generation in range(generations):
			temperture = 100/(generation+1)
			new_population = []
			checkData(population, generation, disInterval)
			boltz_sum = boltzSum(population, temperture)
			while len(new_population) < len(population):
				m = boltzmannSelect(population, temperture, boltz_sum)
				f = boltzmannSelect(population, temperture, boltz_sum)
				if random.random() > pC:
					new_population.append(mutate(chars, m, pM))
					new_population.append(mutate(chars, f, pM))
				else:
					new_population.append(mutate(chars, crossover(m, f), pM))
					new_population.append(mutate(chars, crossover(m, f), pM))
			population = new_population
	else:
		argumentError()
	
	#final report
	best = ""
	best_fitness = 0
	for individual in population:
		if fitness(individual) > best_fitness:
			best = individual
			best_fitness = fitness(individual)
	print("Missed the target")
	print("The best individual is " + best + " with fitness " + str(best_fitness * 100/ len(TARGET)))


def checkData(population, generation, disInterval):
	for individual in population:
		if fitness(individual) == len(TARGET):
			success(individual, generation)
	if (generation / disInterval == math.floor(generation / disInterval)):
		best = ""
		best_fitness = 0
		for individual in population:
			if fitness(individual) > best_fitness:
				best = individual
				best_fitness = fitness(individual)
		print("We're on generation " + str(generation))
		print("The best individual is " + best + " with fitness " + str(best_fitness * 100/ len(TARGET)))

def boltzSum(population, temperture):
	boltz_sum = 0
	for individual in population:
		boltz_sum += math.exp(fitness(individual) / temperture)
	return boltz_sum

def fitness(individual):
	fitness = 0
	for i in range(len(TARGET)):
		if individual[i] == TARGET[i]:
			fitness += 1
	return fitness


def mutate(chars, individual, pM):
	for i in range(len(individual)):
		if random.random() < pM:
			individual = list(individual)
			individual[i] = random.choice(chars)
			individual = "".join(individual)
	return individual

def crossover(m, f):
	individual = ""
	for i in range(len(TARGET)):
		if (random.random() < 0.5):
			individual += m[i]
		else:
			individual += f[i]
	return individual

def populate(population, chars, length):
	individual = ''.join(random.choice(chars) for i in range(length))
	population.append(individual)

def argumentError():
	print("Argument Error: please provide arguments in the specified format.")
	sys.exit()

def noSelectError():
	print("Selection Error: It appears your selection method failed to choose an individual.")
	sys.exit()

def success(individual, generation):
	print("Success!")
	print("Target: " + TARGET)
	print("Individual: " + individual)
	print("Generation achieved: " + str(generation))
	sys.exit()

def tournamentSelect(population):
	best = ""
	second_best = ""
	best_fitness = 0
	second_fitness = 0
	tournament_pop = []
	for i in range(math.floor(len(population) * 0.2)):
		#0.2 was chosen arbitrarily and can be changed
		tournament_pop.append(random.choice(population))
	for individual in tournament_pop:
		if fitness(individual) >= best_fitness:
			second_best = best
			second_fitness = best_fitness
			best = individual
			best_fitness = fitness(individual)
		elif fitness(individual) >= second_fitness:
			second_fitness = fitness(individual)
			second_best = individual
	return best, second_best

def rankSelect(population):
	target = random.random()
	fit_so_far = 0
	for position in range(len(population)):
		fit_so_far += ((position + 1) / (len(population) * (len(population) + 1) / 2))
		if fit_so_far >= target:
			return population[position]
	noSelectError()

def boltzmannSelect(population, temperture, boltz_sum):
	target = random.random()
	fit_so_far = 0
	for individual in population:
		fit_so_far += (math.exp(fitness(individual) / temperture) / boltz_sum)
		if fit_so_far >= target:
			return individual
	noSelectError()
	

if __name__ == '__main__':
	main(sys.argv[1:])
