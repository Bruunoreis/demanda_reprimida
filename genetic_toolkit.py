import random
import linecache
import copy
from collections import namedtuple


# Classe para representar processos biológicos
class BiologicalProcessManager:
		'''
			Função de cruzamento
			- O processo de cruzamento de um ponto é exercido nesta função.
		'''
		def crossover(crossover_rate, parentOne, parentTwo):
			random_probability = random.random()

			if random_probability < crossover_rate:
				return (parentOne, parentTwo)
			else:
				pivot = random.randint(0, len(parentOne.genotype_representation)-1)

				child_one_genotype = parentOne.genotype_representation[:pivot] + parentTwo.genotype_representation[pivot:]
				child_two_genotype = parentTwo.genotype_representation[:pivot] + parentOne.genotype_representation[pivot:]

				child_one = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_one_genotype)
				child_two = Chromosome(parentOne.numberOfKnapsacksReference, parentOne.numberOfObjectsReference, child_two_genotype)

				child_one.phenotype_representation = parentOne.phenotype_representation
				child_two.phenotype_representation = parentOne.phenotype_representation


				return (child_one, child_two)

		'''
			Função de mutação
			- O processo de Reinicialização Aleatória é exercido nesta função.
		'''
		def mutate(mutation_rate, child, numberOfKnapsacks):
			for index, position in enumerate(child.genotype_representation):
				random_probability = random.random()
				'''
					(Reinicialização aleatória) "Inverta" a posição com outra mochila se probabilidade < taxa_mutação
				'''
				if random_probability < mutation_rate:
					child.genotype_representation[index] = random.randint(0,numberOfKnapsacks)


# Classe para representar o cromossomo
class Chromosome:

	fitness = None # Aptidão cromossômica
	phenotype_representation = None # Representação do fenótipo

	def __init__(self, numOfKnapsacks, numOfObjects, genotype_representation = None):
		self.numberOfKnapsacksReference = numOfKnapsacks
		self.numberOfObjectsReference = numOfObjects

		if genotype_representation == None:
			self.genotype_representation = [random.randint(0,(numOfKnapsacks)) for x in range(0, numOfObjects)]
		else:
			self.genotype_representation = genotype_representation

		self.length_of_encoding = len(self.genotype_representation)

	'''
	Gera uma adequação para todos os cromossomos agregando seus benefícios/valores
	'''
	def generateFitness(self, knapsackList):
		''' Faça uma cópia da lista da mochila a ser usada para avaliar se os objetos no cromossomo
		exceda C usando o atributo 'amountUsed'
		'''
 ##sequência de alocações
		#print("ORIGINAL CHROM: {}".format(self.genotype_representation))
		knapsacks = copy.deepcopy(knapsackList)
		fitnessScore = 0
		done = False
		for i, placement_of_object in enumerate(self.genotype_representation):
			if placement_of_object == 0:
				continue
			else:
				for knapsack in knapsacks :         
					if knapsack.id == placement_of_object and knapsack.id == self.phenotype_representation[i].ref :
						# se estiver acima da capacidade, troque de bolsa e reavalie
						if self.phenotype_representation[i].weight > knapsack.capacity:
							while(not done):

								self.genotype_representation[i] = random.randint(0,(self.numberOfKnapsacksReference))

								if self.genotype_representation[i] == 0:
									break
								else:
									current_knapsack = next((sack for sack in knapsacks if sack.id == self.genotype_representation[i]),None)
									if self.phenotype_representation[i].weight > current_knapsack.capacity:
										continue
									if self.phenotype_representation[i].weight <= current_knapsack.capacity:
										fitnessScore += self.phenotype_representation[i].value
										'''Agora subtraímos o peso dos objetos pela capacidade das mochilas
										para que possamos acompanhar quanto espaço a mochila deixou
										no caso de outro objeto entrar na mesma mochila
										'''
									current_knapsack.capacity = (current_knapsack.capacity - self.phenotype_representation[i].weight)
									break
						else:
							fitnessScore += self.phenotype_representation[i].value
							'''Agora subtraímos o peso dos objetos pela capacidade das mochilas
							para que possamos acompanhar quanto espaço a mochila deixou
							no caso de outro objeto entrar na mesma mochila
							'''
							knapsack.capacity = (knapsack.capacity - self.phenotype_representation[i].weight)
				

		
# atualiza o fitness dos cromossomos
		self.fitness = fitnessScore




class Knapsack:
	def __init__(self, id, capacity):
		self.id = id
		self.capacity = capacity

class Population:

	Phenotype = namedtuple('Phenotype', 'id weight value ref')
	knapsackList = [] # lista de mochilas
	knapSackEvaluationList = [] # usado para gerar a aptidão dos cromossomos
	population = []

	def __init__(self, size):
		self.populationSize = size
		self.numberOfKnapsacks = 0

	def select_parents(self,tournament):
		'''
			A seleção do torneio está sendo usada para encontrar dois pais
		'''
		first_fittest_indiv = None
		second_fittest_indiv = None

		for individual in tournament:
			# Verifique se este indivíduo é mais apto que o atual apto
			if first_fittest_indiv == None or individual.fitness > first_fittest_indiv.fitness:
				first_fittest_indiv = individual

		tournament.remove(first_fittest_indiv)

		for individual in tournament:
			# Verifique se este indivíduo é mais apto que o atual apto
			if second_fittest_indiv == None or individual.fitness > second_fittest_indiv.fitness:
				second_fittest_indiv = individual

		#print("FIRST: {},  SECOND: {}".format(first_fittest_indiv.fitness,second_fittest_indiv.fitness))
		return (first_fittest_indiv,second_fittest_indiv)


	def initialize_population(self):
     
     
     
		'''
			Leia de um arquivo e crie os cromossomos
		'''
		# Open data file
		dataFile = open('data_5.txt','r')

		# Leia quantas mochilas haverá. (lemos o primeiro byte)
		numOfKnapsacks = int(dataFile.read(2))
		self.numberOfKnapsacks = numOfKnapsacks
		#print("NUMBER OF KNAPSACKS: {} \n".format(numOfKnapsacks))
		dataFile.seek(0,0);

		# Leia quantos objetos haverá.
		numOfObjects = int(dataFile.readlines()[numOfKnapsacks+1])

		# Cria dicionário de mochila
		lines_to_read = []
		for num in range(0, numOfKnapsacks):
			lines_to_read.append(num)

		dataFile.seek(0,0)
		for i,line in enumerate(dataFile):
			if i == 0:
				continue
			elif i > 0 and i < numOfKnapsacks + 1:
				capacity = int(line)
				self.knapsackList.append(Knapsack((i), capacity))

		# Cria a representação do fenótipo do cromossomo
		phenotype_representation = []
		lineNumberOffset = numOfKnapsacks + 3 # deslocamento de arquivo usado para localizar os objetos no arquivo
		for i in range(0,numOfObjects):
			value,weight,ref = linecache.getline("data_5.txt", lineNumberOffset+i).split()
			# Cria a representação do fenótipo para cada cromossomo
			phenotype_representation.append(self.Phenotype(i, int(value),int(weight),int(ref)))

		# Cria a população inicial
		for j in range(0,self.populationSize):
			# Cria um novo cromossomo
			new_chromosome = Chromosome(numOfKnapsacks,numOfObjects)
			# Dê a cada cromossomo sua representação fenotípica
			new_chromosome.phenotype_representation = phenotype_representation
			# Avalia cada cromossomo
			new_chromosome.generateFitness(self.knapsackList)
			# Adiciona o cromossomo à população
			self.population.append(new_chromosome)

		dataFile.close()
