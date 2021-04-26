from phantom import *
import numpy as np
from sklearn.preprocessing import normalize

#preferences should be listed by good not by agent, so 
#[[0.2,0.3,0.4], [0.8,0.7,0.6]]
# has two (2) goods and three (3) agents participating

def generate_preferences(a, n):
    data = np.random.rand(a, n)
    data = normalize(data, axis=0, norm='l1')
    return data

goods = 10 # number og goods
n =  20 # number of agents

def proportional_phantoms(t):
	phantoms = np.ones(n+1) 
	for j in range(n + 1):
		phantoms[j] = min(t*(n-j), 1)
	return np.broadcast_to(phantoms,(goods,len(phantoms)))

def welfare_phantoms(t):
	phantoms = np.ones(n+1) 
	for j in range(n + 1):
		if(t <= j/(n+1)):
			phantoms[i][j] = 0
		elif((j+1)/(n+1)<= t):
			phantoms[i][j] = t * (n+1) - j
	return np.broadcast_to(phantoms,(goods,len(phantoms)))

pref = generate_preferences(goods, n)
print('preferences', pref)
allocation, t = get_feasible_allocation(pref, proportional_phantoms)
k = 4
idx = (-allocation).argsort()[:k]
print('K commitee', idx)

opt_alloc = np.sum(pref, axis=1)
idx_opt = (-opt_alloc).argsort()[:k]
print('Commitee by weights', idx_opt)