import numpy as np

SEARCH_LENGTH = 200

def compute_allocation(preferences, phantoms):
	big_array = np.concatenate((preferences, phantoms), axis = 1)
	allocation = np.median(big_array, axis = 1)
	return allocation

def get_feasible_allocation(preferences, phantom_function):
	start = 0.0
	end = 1.0


	test_alloc = compute_allocation(preferences, phantom_function(start))
	start_val = np.sum(test_alloc)
	if start_val > 1.0:
		raise ValueError("Allocation with t=0 was not feasible")

	test_alloc = compute_allocation(preferences, phantom_function(end))
	end_val = np.sum(test_alloc)
	if end_val <= 1.0:
		print("Little weirdness happening here, t=1.0 is the solution?")
		return test_alloc

	for i in range(SEARCH_LENGTH):
		approx_slope = (end_val - start_val) / (end - start)
		t = end - (end_val - 1) / approx_slope

		test_alloc = compute_allocation(preferences, phantom_function(t))
		mid_val = np.sum(test_alloc)
		if mid_val == 1.0:
			return test_alloc,t

		else:
			if mid_val < 1.0:
				start = t
				start_val = mid_val
			else:
				end = t
				end_val = mid_val








