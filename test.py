from phantom import *
import numpy as np

#preferences should be listed by good not by agent, so 
#[[0.2,0.3,0.4], [0.8,0.7,0.6]]
# has two (2) goods and three (3) agents participating
preferences = np.array([[0.2,0.3,0.4], [0.8,0.7,0.6]])
print(np.median(preferences, axis = 1))


def test_phantoms(t):
	return np.ones((2,3)) * t

print(get_feasible_allocation(preferences, test_phantoms))