# Adaptado den Guled em https://github.com/Somnibyte/Multiple-Knapsack-Problem-Genetic-Algorithm
# Problema: Multiplas Mochilas


from genetic_toolkit import Population,Chromosome,BiologicalProcessManager
import statistics
import random

'''
	Função de avaliação de geração
'''
def find_the_best(population):
	best = None
	for individual in population:
		if best == None or individual.fitness > best.fitness:
			best = individual
	return best.fitness

# Variáveis globais
crossover_rate = 0.165


# Inicializa a população com soluções candidatas aleatórias
population = Population(700)
population.initialize_population()

# Defina a taxa de mutação
mutation_rate = 2.2/population.populationSize

# Obter uma referência ao número de mochilas
numberOfKnapsacks = population.numberOfKnapsacks


generation_counter = 0
while(generation_counter != 100):
	current_population_fitnesses = [chromosome.fitness for chromosome in population.population]
	print("CURRENT GEN FITNESS: {} \n ".format(current_population_fitnesses))
	new_gen = []
	while(len(new_gen) != population.populationSize):
		
		# Criar torneio para processo de seleção de torneio
		tournament = [population.population[random.randint(1, population.populationSize-1)] for individual in range(1, population.populationSize)]
		# Obtenha dois pais no processo de seleção do torneio
		parent_one, parent_two = population.select_parents(tournament)
		# Cria a descendência desses dois pais
		child_one,child_two = BiologicalProcessManager.crossover(crossover_rate,parent_one,parent_two)

		# Tente transformar as crianças
		BiologicalProcessManager.mutate(mutation_rate, child_one, numberOfKnapsacks)
		BiologicalProcessManager.mutate(mutation_rate, child_two, numberOfKnapsacks)

		# Avalie cada uma das crianças
		child_one.generateFitness(population.knapsackList)
		child_two.generateFitness(population.knapsackList)

		# Adicione os filhos à nova geração de cromossomas
		new_gen.append(child_one)
		new_gen.append(child_two)

	# Substitua a geração antiga pela nova
	population.population = new_gen
	generation_counter += 1
