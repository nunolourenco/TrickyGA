import random
from copy import deepcopy
from operator import itemgetter

def load_files():
	def int_list(value):
		l = []
		result = value.split()
		for r in result:
			l.append(int(r))
		return l
	cards = {}
	f = open("puzzle.txt", "r")
	lines = f.readlines()
	lines = lines[1: ]
	count = 0
	for el in lines:
		cards[count] = int_list(str(el[:-2]))
		count += 1
	return cards
	
def get_card(el, dictio):
	card = deepcopy(dictio[el[0]])
	#el[1] card rotation
	for i in range(el[1]):
		temp = []
		last = card[-1]
		for i in card[ : -1]:
			temp.append(i)
		temp.insert(0,last)
		card = deepcopy(temp)
		#print card
	return card
		
def fenotype(ind, dictio):
	#print len(ind)
	puzzle = []
	count = 0;
	temp = []
	for el in ind:
		if count != 0 and count % 6 == 0:
			puzzle.append(temp)
			#print temp
			temp = []
		temp.append(get_card(el, dictio))
		temp
		count += 1
	else:
		puzzle.append(temp)	
	#print len(puzzle)
	return puzzle
	
	

		
def evaluate(ind, dictio):
	
	def check_north(i,j,puzzle):
		if(i == 0):
			return 1
		else:
			curr = puzzle[i][j]
			north = puzzle[i-1][j]
			if(curr[0] == north[0] and curr[1] == north[1]):
				return 1
			else:
				return 0
				
	def check_east(i,j,puzzle):
		#print"(%d,%d)" % (i,j)
		#print len(puzzle) - 1
		#print j == len(puzzle) - 1
		if(j == len(puzzle) - 1):
			return 1
		else:
			curr = puzzle[i][j]
			east = puzzle[i][j + 1]
			if curr[1] == east[0] and curr[2] == east[3]:
				return 1
			else:
				return 0 	
	def check_south(i,j,puzzle):
		if(i == len(puzzle) - 1):
			return 1
		else:
			curr = puzzle[i][j]
			south = puzzle[i+1][j]
			if(curr[2] == south[1] and curr[3] == south[0]):
				return 1
			else:
				return 0
	def check_west(i,j,puzzle):
		if(j == 0):
			return 1
		else:
			curr = puzzle[i][j]
			west = puzzle[i][j - 1]
			if curr[0] == west[1] and curr[3] == west[2]:
				return 1
			else:
				return 0
	puzzle = fenotype(ind, dictio)
	
	#print len(puzzle)
	
	fitness = 0
	
	for i in range(len(puzzle)):
		s = 0
		for j in range(len(puzzle[i])):
			#print len(puzzle[i])
			s += check_north(i,j,puzzle)
			s += check_east(i,j,puzzle)
			s += check_south(i,j,puzzle)
			s += check_west(i,j,puzzle)
			if(s == 4):
				fitness += 1
	return fitness



def apply_mutation_rotate(ind, prob_mut):
	mutated = []
	for i in ind:
		new_ind = i
		if random.random() < prob_mut:
			new_ind = (i[0], random.choice(range(4)))
		mutated.append(new_ind)
	return mutated


def apply_mutation_swap(ind):
	new_ind = deepcopy(ind)
	i = random.randint(0,len(ind) - 1)
	j = random.randint(0,len(ind) - 1)
	while i == j:
		i = random.randint(0,len(ind) - 1)
		j = random.randint(0,len(ind) - 1)
		new_ind[i],new_ind[j] = new_ind[j], new_ind[i]
	return new_ind

def roulette_wheel(population, numb):
	pop = population[:]
	pop.sort(key=itemgetter(1))
	total_fitness = sum([indiv[1] for indiv in pop])
	mate_pool = []
	for i in range(numb):
		value = random.uniform(0,1)
		index = 0
		total = pop[index][1]/ float(total_fitness)
		while total < value:
			index += 1
			total += pop[index][1]/ float(total_fitness)
		mate_pool.append(pop[index])
	return mate_pool
	
def order_xover(mate_pool, dictio):
	def build_offspring(p1, p2, c1, c2):
		def exists(v, a):
			for el in a:
				if v[0] == el[0] and el[0] != -1:
					return True
			return False
		
		#print "building offspring"
		off = [ (-1,-1) for i in range(len(p1))]
		off[c1 : c2 + 1] = p1[c1 : c2 + 1]
		elements_copied = c2 - c1
		parent_pos = (c2 + 1) % len(p2)
		offspring_pos = (c2 + 1) % len(p2)
		while elements_copied < len(p2) - 1:	
			temp = p2[parent_pos]
			parent_pos = (parent_pos + 1) % len(p2)
			if(exists(temp,off)):
				continue
			else:	
				off[offspring_pos] = temp
				offspring_pos = (offspring_pos + 1) % len(p2)
			 	elements_copied += 1
			
		return off	 
				
	first_point = random.randint(0,len(mate_pool[0][0]) / 2)
	second_point = random.randint(first_point + 1,len(mate_pool[0][0]) - 1)
	offsprings = []
	for i in range(0,len(mate_pool),2):
		p1 = mate_pool[i][0]
		p2 = mate_pool[i + 1][0]
		off1 = build_offspring(p1, p2, first_point, second_point)
		off2 = build_offspring(p2, p1, first_point, second_point)
		offsprings.append((off1,0))
		offsprings.append((off2,0))
	offsprings = [(off[0], evaluate(off[0], dictio)) for off in offsprings]
	offsprings.sort(key=itemgetter(1), reverse = True)
	return offsprings
		



def generate_population(dictio, pop_size):
	card_number = len(dictio.keys())
	population = []
	for i in range(pop_size):
		cards = []
		count = 0
		while count < card_number:
			card = random.randint(0,card_number-1)
			if card not in cards:
				cards.append(card)
				count += 1
		ind = ([ (cards[i], random.choice(range(4))) for i in range(card_number) ],0)
		population.append(ind)
	return population
	
	
def ga(runs, dictio, pop_size, prob_mut_swap, prob_mut_rot):
	iteration = 0
	population = generate_population(dictio, pop_size)	
	#print len(population)
	population = [(ind[0], evaluate(ind[0], dictio)) for ind in population]
	population.sort(key=itemgetter(1), reverse = True)
	#print population
	while iteration < runs:
		iteration += 1
		print iteration
		mate_pool = roulette_wheel(population, len(population))		
		#generate_offsprings
		new_population = order_xover(mate_pool, dictio)
		offsprings = []
		#apply rotation mutation
		for ind,fit in new_population:
			new_ind = ind
			if random.random() < prob_mut_rot:
				new_ind = apply_mutation_rotate(ind, prob_mut_rot)
			#print len(new_ind)
			if random.random() < prob_mut_swap:
				new_ind = apply_mutation_swap(ind)
			offsprings.append((new_ind,0))
		#half of the best parents go on to the next generation
		best = population[ : len(population) / 2]
		population = deepcopy(offsprings[ : (len(offsprings) / 2)])
		population.extend(best)
		#print len(population)
		#print population
		population = [(ind[0], evaluate(ind[0], dictio)) for ind in population]
		population.sort(key=itemgetter(1), reverse = True)		
		print "Well positioned cards: ",
		print population[0][1]
		
	return population[0]








		
cards = load_files()
#print cards
best_solution = ga(1000,cards,100,0.40,0.8)

print best_solution