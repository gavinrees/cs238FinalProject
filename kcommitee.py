from phantom import *
import numpy as np
from sklearn.preprocessing import normalize
import random

#preferences should be listed by good not by agent, so 
#[[0.2,0.3,0.4], [0.8,0.7,0.6]]
# has two (2) goods and three (3) agents participating

def generate_uniform_preferences(a, n):
    data = np.random.rand(a, n)
    data = normalize(data, axis=0, norm='l1')
    return data

def preference_from_ranking_vec(ranking_list):
	denom = 1 - 1 / (2 ** len(ranking_list))
	prefs = np.ones(len(ranking_list)) * 0.5
	prefs = prefs ** np.array(ranking_list)
	return prefs / denom


def geopreference_from_ranking_mat(ranking_mat):
	denom = 1 - 1 / (2 ** ranking_mat.shape[1])
	prefs = np.ones(ranking_mat.shape) * 0.5
	exps = np.arange(ranking_mat.shape[1]) + 1
	exps = np.broadcast_to(exps, ranking_mat.shape).copy()


	# print("exps: ", exps)
	# print("ranking_mat: ", ranking_mat)
	# exps[0,:] = exps[0, ranking_mat[0,:] - 1]
	for i in range(exps.shape[0]):
		for j in range(exps.shape[1]):
			r = int(ranking_mat[i,j])
			exps[i, r-1] = j + 1
		# print(exps[i,:])
		# print(ranking_mat[i,:] - 1)
		# exps[i,:] = exps[i, ranking_mat[i,:] - 1]


	prefs = prefs ** exps
	return prefs / denom

def arithpreference_from_ranking_mat(ranking_mat):
	a = ranking_mat.shape[1]
	denom = a * (a + 1) / 2.0

	coeffs = np.zeros(ranking_mat.shape)

	for i in range(coeffs.shape[0]):
		for j in range(coeffs.shape[1]):
			r = int(ranking_mat[i,j])
			coeffs[i, r-1] = (a - j) / denom

	return coeffs



def harmpreference_from_ranking_mat(ranking_mat):
	a = ranking_mat.shape[1]
	denom = sum([1 / (1.0 * i) for i in range(1,a + 1)])

	coeffs = np.zeros(ranking_mat.shape)

	for i in range(coeffs.shape[0]):
		for j in range(coeffs.shape[1]):
			r = int(ranking_mat[i,j])
			coeffs[i, r-1] = (1/(j+1)) / denom

	return coeffs








row_shuffle = np.vectorize(np.random.permutation, signature='(n)->(n)')


def generate_random_rankings(a,n):
	l = np.arange(a) + 1
	l = np.broadcast_to(l, (n,a)).copy()
	l = row_shuffle(l)
	return l

def generate_ranked_preferences(a,n):
	l = generate_random_rankings(a,n)
	return np.transpose(preference_from_ranking_mat(l))



def generate_psc_ranking(a,n, k, l):
	ranking_list = []

	size = int(np.ceil(n/(k * 1.0) * l))
	for i in range(size):
		first = [j+ 1 for j in range(l)]
		random.shuffle(first)
		second = [j + 1 for j in range(l, a)]
		random.shuffle(second)
		ranking_list.append(first + second)

	for i in range(n - size):
		rank = [j + 1 for j in range(a)]
		random.shuffle(rank)
		ranking_list.append(rank)

	return ranking_list


def stv(ranking_list, k):
	# money = [1.0 for i in range(len(ranking_list))]
	num_candidates = len(ranking_list[0])
	num_voters = len(ranking_list)
	committee = []
	eliminated = set()

	while len(committee) < k:
		# print("current committee at top: " + str(committee))
		# print("current rankings: ", ranking_list)
		# candidate_budgets = [0.0 for i in range(num_candidates)]
		num_supporters = [0 for i in range(num_candidates)]
		for i, ranking in enumerate(ranking_list):
			# candidate_budgets[ranking[0] - 1] += money[i]
			num_supporters[ranking[0]-1] += 1

		# biggest_budget = max(candidate_budgets)
		biggest_support = max(num_supporters)
		# print("candidate budgets: ", candidate_budgets)
		# print("biggest_budget: ", biggest_budget)
		# print("candidate supporters: ", num_supporters)
		# print("biggest_support: ", biggest_support)

		eliminating = -1
		# if biggest_budget >= num_voters / k:
		if biggest_support >= num_voters / k:
			i = 0
			# while candidate_budgets[i] < biggest_budget:
			while num_supporters[i] < biggest_support:
				i += 1

			committee.append(i)
			# print(i)

			# for j, r in enumerate(ranking_list):
			# 	if r[0] == i + 1:
			# 		# money[j] -= (num_voters / (k * 1.0)) / num_supporters[i]
			# 		if money[j] < 0.0:
			# 			raise Exception("Someone went to negative money")



			eliminating = i

		else:
			min_el = -1
			min_el_val = num_candidates * 1.0
			# for i, v in enumerate(candidate_budgets):
			for i, v in enumerate(num_supporters):
				if i not in eliminated:
					if v < min_el_val:
						min_el = i
						min_el_val = v

			eliminating = min_el


		eliminated.add(eliminating)
		for j in range(num_voters):
			if eliminating + 1 in ranking_list[j]:
				ranking_list[j].remove(eliminating + 1)

	return [c + 1 for c in committee]

def phantom_committee_select(ranking_list, k, budgetrule = "geo"):
	a = len(ranking_list[0])
	n = len(ranking_list)
	prefs = None
	if budgetrule == "geo":
		prefs = geopreference_from_ranking_mat(np.array(ranking_list))
	elif budgetrule == "arith":
		prefs = arithpreference_from_ranking_mat(np.array(ranking_list))
	elif budgetrule == "harm":
		prefs = harmpreference_from_ranking_mat(np.array(ranking_list))
	else:
		raise Exception("Budget rule " + str(budgetrule) + " doesn't exist")
	prefs = np.transpose(prefs)
	alloc,t = get_feasible_allocation(prefs, moving_market_phantom(a,n))
	# print(alloc)
	idx = (-alloc).argsort()[:k] + 1
	return idx.tolist()

# def stv(rankings):



# example = np.array([[1,2,3,4,5,6], [6,2,5,1,4,3]])
# print("Example: ", example)
# print("geopreference_from_ranking_mat: ", geopreference_from_ranking_mat(example))

# example = np.array([[1,2,3,4,5,6], [6,2,5,1,4,3]])
# print("Example: ", example)
# print("arithpreference_from_ranking_mat: ", arithpreference_from_ranking_mat(example))

# example = np.array([[1,2,3,4,5,6], [6,2,5,1,4,3]])
# print("Example: ", example)
# print("arithpreference_from_ranking_mat: ", harmpreference_from_ranking_mat(example))

print("Generating PSC ranking with a = 5, n = 10, k = 3, l = 2")
print(generate_psc_ranking(5,10,3,2))






# goods = 10 # number og goods
# n =  20 # number of agents

# def proportional_phantoms(t):
# 	phantoms = np.ones(n+1) 
# 	for j in range(n + 1):
# 		phantoms[j] = min(t*(n-j), 1)
# 	return np.broadcast_to(phantoms,(goods,len(phantoms)))

# def welfare_phantoms(t):
# 	phantoms = np.ones(n+1) 
# 	for j in range(n + 1):
# 		if(t <= j/(n+1)):
# 			phantoms[i][j] = 0
# 		elif((j+1)/(n+1)<= t):
# 			phantoms[i][j] = t * (n+1) - j
# 	return np.broadcast_to(phantoms,(goods,len(phantoms)))

# pref = generate_preferences(goods, n)
# print('preferences', pref)
# allocation, t = get_feasible_allocation(pref, proportional_phantoms)
# k = 4
# idx = (-allocation).argsort()[:k]
# print('K commitee', idx)

# opt_alloc = np.sum(pref, axis=1)
# idx_opt = (-opt_alloc).argsort()[:k]
# print('Commitee by weights', idx_opt)