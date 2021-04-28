import kcommitee as kcom
import phantom as phant
import numpy as np 
import random

"""
implemented without the funkyness in the slide about budgets -- I think that's
more of a proof-oriented way to look at it that isn't actually useful for implmentation
"""


"""
some test code here!


example_rankings = [[1,2,3],[2,1,3], [2,3,1]]
print("Running stv on: ", example_rankings)
print(stv(example_rankings, 2))
example_rankings = [[1,2,3],[1,2,3], [2,3,1]]
print("Runninng phantom_committee_select on : ", example_rankings)
print(phantom_committee_select(example_rankings, 2))

""" 

def test_committee_equal(com1, com2):
	if len(com1) != len(com2):
		return False
	for i in com1:
		if i not in com2:
			return False

	return True

def committee_diff(com1,com2):
	x = 0
	for i in com1:
		if i not in com2:
			x += 1

	return x

def testPSCholds(l, com):
	for i in range(l):
		if i + 1 not in com:
			# print(l + 1)
			# print(com)
			return False

	return True

print("testPSCholds check")
print(testPSCholds(1, [1]))




NUM_TRIALS = 10000
TRIAL_A = 5
TRIAL_N = 11
TRIAL_K = 3




for l in range(1,3):

	count = 0
	num_examples_reported = 0
	for i in range(NUM_TRIALS):
		if i % 2000 == 0:
			print(i)
		ranking_list = kcom.generate_psc_ranking(TRIAL_A, TRIAL_N, TRIAL_K, l)
		phantom_com = kcom.phantom_committee_select(ranking_list, TRIAL_K, budgetrule="harm")
		if testPSCholds(l,phantom_com):
			count +=1
		else:
			if num_examples_reported < 6:
				print("Found a PSC counterexample for l = ", l)
				print("Ranking is :", ranking_list)
				print("Committee is: ", phantom_com)
				myphant = phant.moving_market_phantom(TRIAL_A, TRIAL_N)
				prefs = kcom.geopreference_from_ranking_mat(np.array(ranking_list))
				print("Allocation is: ", phant.get_feasible_allocation(np.transpose(prefs), myphant ))
				num_examples_reported += 1

	print("Found ", NUM_TRIALS - count, " counterexamples for l = ", l)


# print("Agreement is: ", count * 1.0 / NUM_TRIALS * 100, "%")
# print("Nearness among disagreements is: ", nearness / (NUM_TRIALS - count) * 100, "%")


