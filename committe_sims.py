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




NUM_TRIALS = 10000
TRIAL_A = 15
TRIAL_N = 80
TRIAL_K = 5


count = 0
nearness = 0.0
for i in range(NUM_TRIALS):
	if i % 5000 == 0:
		print(i)
	ranking_list = kcom.generate_random_rankings(TRIAL_A, TRIAL_N)
	ranking_list = ranking_list.tolist()
	phantom_com = kcom.phantom_committee_select(ranking_list, TRIAL_K, budgetrule="geo")
	# stv_com = kcom.stv(ranking_list, TRIAL_K)
	stv_com = kcom.phantom_committee_select(ranking_list, TRIAL_K, budgetrule="harm")
	if test_committee_equal(stv_com, phantom_com):
		count +=1
	else:
		nearness += (1- committee_diff(phantom_com, stv_com) * 1.0 / TRIAL_K)


print("Agreement is: ", count * 1.0 / NUM_TRIALS * 100, "%")
print("Nearness among disagreements is: ", nearness / (NUM_TRIALS - count) * 100, "%")


