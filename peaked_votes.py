import kcommitee as kcom
import numpy as np


M = 5
master_means = kcom.generate_random_rankings(M, 1)
master_means = kcom.arithpreference_from_ranking_mat(master_means)
def generate_single_peaked(N):
	prefs = np.ones((N,M))
	for i in range(N):
		prefs[i,:] = np.random.normal(master_means, 0.5/M)
		for j in range(M):
			if prefs[i,j] < 0.0:
				prefs[i,j] = 0.0

		prefs[i,:] = prefs[i,:] / np.sum(prefs[i,:])

	return prefs


print(generate_single_peaked(3))
