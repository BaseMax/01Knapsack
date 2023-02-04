def knapsack_dynamic(weights, values, capacity):
	# Get the number of items
	n = len(values)

	# Create a 2D array to store the maximum value that can be obtained for each capacity and item
	K = [[0 for x in range(capacity + 1)] for x in range(n + 1)]

	# Loop through each item
	for i in range(n + 1):
		# Loop through each capacity
		for c in range(capacity + 1):
			# If either the item or the capacity is 0, set the maximum value to 0
			if i == 0 or c == 0:
				K[i][c] = 0
			# If the current item can be added to the knapsack without exceeding the capacity, compare the maximum value obtained by adding the current item to the knapsack and the maximum value obtained without adding the current item
			elif c >= weights[i-1]:
				K[i][c] = max(values[i-1] + K[i-1][c-weights[i-1]],  K[i-1][c])
			# If the current item cannot be added to the knapsack without exceeding the capacity, the maximum value is the same as the maximum value obtained without adding the current item
			else:
				K[i][c] = K[i-1][c]

	# Return the maximum value that can be obtained with the given items and capacity
	return K[n][capacity]

# Divide and Conquer
def knapsack_divide_conquer(wt, val, w):
	# If the knapsack has no capacity or there are no items to choose from, return 0
	if w == 0 or len(wt) == 0:
		return 0

	# If there is only one item, check if it fits in the knapsack and return its value
	if len(wt) == 1:
		if wt[0] <= w:
			return val[0]
		else:
			return 0

	# If there are multiple items, choose the maximum value between two options:
	# - including the first item in the knapsack and checking the remaining items with reduced capacity
	# - not including the first item and checking the remaining items with the same capacity
	return max(
		val[0] + knapsack_divide_conquer(wt[1:], val[1:], w-wt[0]),
		knapsack_divide_conquer(wt[1:], val[1:], w)
	)

# Greedy Algorithm
# def knapsack_greedy(wt, val, w):
# 	n = len(val)
# 	ratio = []
# 	for i in range(0,n):
# 		ratio.append(val[i]/wt[i])

# 	for i in range(0,n):
# 		for j in range(0,n - i - 1):
# 			if ratio[j] < ratio[j + 1]:
# 				ratio[j], ratio[j + 1] = ratio[j + 1], ratio[j]
# 				wt[j], wt[j + 1] = wt[j + 1], wt[j]
# 				val[j], val[j + 1] = val[j + 1], val[j]

# 	totalValue = 0
# 	for i in range(0,n):
# 		if wt[i] <= w:
# 			totalValue += val[i]
# 			w -= wt[i]
# 		else:
# 			break
# 	return totalValue

# def knapsack_greedy(weights, values, capacity):
# 	# Get the number of items
# 	n = len(values)

# 	# Create a list to store the value-to-weight ratios of each item
# 	ratios = [(v/w, v, w) for v, w in zip(values, weights)]
  
# 	# Sort the list of ratios in descending order based on the ratio
# 	ratios.sort(reverse=True)

# 	# Initialize the total value
# 	total_value = 0

# 	# Loop through each item
# 	for v, w in [(v, w) for r, v, w in ratios if w <= capacity]:
# 		# If the current item can be added to the knapsack without exceeding the capacity, add its value to the total value and reduce the capacity by its weight
# 		total_value += v
# 		capacity -= w
# 		# If the knapsack is filled to capacity, break the loop
# 		if capacity == 0:
# 			break
  
# 	# Return the total value of items in the knapsack
# 	return total_value

def knapsack_greedy(wt, val, w):
	n = len(val)
	ratio = []
	
	# Calculate the value-to-weight ratio of each item
	for i in range(n):
		ratio.append(val[i] / wt[i])
		
	# Sort the items based on their value-to-weight ratio in descending order
	for i in range(n):
		for j in range(0, n-i-1):
			if ratio[j] < ratio[j+1]:
				ratio[j], ratio[j+1] = ratio[j+1], ratio[j]
				wt[j], wt[j+1] = wt[j+1], wt[j]
				val[j], val[j+1] = val[j+1], val[j]
				
	# Select items for the knapsack based on the sorted list of items
	total_value = 0
	for i in range(n):
		if wt[i] <= w:
			total_value += val[i]
			w -= wt[i]
		else:
			break
	return total_value

# Branch and Bound
# The branch and bound method is a systematic method for solving the 0-1 knapsack problem. It involves dividing the problem into smaller subproblems and exploring them in a specific order to determine the optimal solution.
# Here are the three different approaches to the branch and bound method for the 0-1 knapsack problem:
# - First Depth: In this approach, we use a stack data structure to keep track of the subproblems we have to solve. At each step, we choose the next subproblem to solve by removing the last subproblem from the stack. This approach continues until we have found the optimal solution or all subproblems have been explored.
# - First Breadth: In this approach, we use a queue data structure to keep track of the subproblems we have to solve. At each step, we choose the next subproblem to solve by removing the first subproblem from the queue. This approach continues until we have found the optimal solution or all subproblems have been explored.
# - First Best: In this approach, we use a priority queue data structure to keep track of the subproblems we have to solve. At each step, we choose the next subproblem to solve by removing the subproblem with the highest priority from the queue. This approach continues until we have found the optimal solution or all subproblems have been explored.
class Node:
	def __init__(self, level, value, weight, bound):
		self.level = level 
		self.value = value 
		self.weight = weight 
		self.bound = bound 

def boundValue(node, n, w, val, wt): 
	# If the weight of the node is greater than or equal to the maximum weight, return 0
	if node.weight >= w: 
		return 0
  
	# Initialize the bound value to the value of the node
	bound = node.value 
	# Initialize the level of the node to the next item
	j = node.level + 1
	# Initialize the total weight to the weight of the node
	totalWeight = node.weight
 
	# Check if the total weight plus the weight of the current item is less than or equal to the maximum weight
	while (j < n and totalWeight + wt[j] <= w): 
		# If so, add the weight of the current item to the total weight
		totalWeight += wt[j] 
		# And add the value of the current item to the bound value
		bound += val[j] 
		# Move on to the next item
		j += 1
  
	# If there are still items left, add the value of the fractional item to the bound value
	if j < n: 
		bound += (w - totalWeight) * val[j]/wt[j]
 
	# Return the calculated bound value
	return bound 

# First Depth
# In this method, we use a stack to keep track of the nodes in the search tree and explore the tree in a depth-first manner. 
# At each node, we calculate the bound value and if it is greater than the maximum value found so far, 
# we add the right child node to the stack. 
# If the left child node results in a weight that is less than or equal to the knapsack capacity and 
# a value greater than the maximum value, we update the maximum value.
def knapsack_first_depth(wt, val, w):
	# number of items
	n = len(val)
	# keep track of the maximum value found so far
	maxValue = 0
	# create a new node with level -1, value 0, weight 0, and flag 0
	node = Node(-1, 0, 0, 0)
	# create a stack to keep track of the nodes in the search tree
	stack = []
	# add the node to the stack
	stack.append(node)
	# keep looping until the stack is empty
	while len(stack) != 0:
		# remove the last node from the stack
		node = stack.pop()
		# if the node level is equal to the number of items - 1
		if node.level == n - 1:
			# continue to the next iteration
			continue
		# create a left node by adding the value and weight of the current node with the next item
		left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0)
		if left.weight <= w and left.value > maxValue:
			# if the weight of the left node is less than or equal to the knapsack capacity and
			# the value of the left node is greater than the maximum value found so far
			maxValue = left.value # update the maximum value with the value of the left node
		# create a right node with the same value and weight as the current node
		right = Node(node.level + 1, node.value, node.weight, 0)
		# calculate the bound value of the right node
		bound = boundValue(right, n, w, val, wt)
		# if the bound value of the right node is greater than the maximum value found so far
		if bound > maxValue:
			# add the right node to the stack
			stack.append(right)
		# add the left node to the stack
		stack.append(left)
	# return the maximum value found
	return maxValue

# First Breadth
# In this method, we use a queue to keep track of the nodes in the search tree and explore the tree in a breadth-first manner. 
# At each node, we calculate the bound value and if it is greater than the maximum value found so far, 
# we add the right child node to the queue. We always add the left child node to the queue.
def knapsack_first_breadth(wt, val, w): 
	# number of items
	n = len(val)
	# keep track of the maximum value found so far
	maxValue = 0
	# create a new node with level -1, value 0, weight 0, and flag 0
	node = Node(-1, 0, 0, 0)
	# create a queue to keep track of the nodes in the search tree
	queue = []
	# append the node to the queue
	queue.append(node)
	# keep looping until the queue is empty
	while len(queue) != 0:
		# remove the node from the front of the queue
		node = queue.pop(0)
		# if the node level is equal to n - 1, continue to the next iteration
		if node.level == n - 1:
			continue
		# create the left child node by adding the value and weight of the current node and the item in the next level
		left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0) 
		if left.weight <= w and left.value > maxValue: # if the weight is less than or equal to the knapsack capacity and the value is greater than the maximum value
			maxValue = left.value # update the maximum value
		# create the right child node by only adding the level and keeping the value and weight the same as the current node
		right = Node(node.level + 1, node.value, node.weight, 0) 
		# calculate the bound value for the right child node
		bound = boundValue(right, n, w, val, wt)
		# if the bound value is greater than the maximum value
		if bound > maxValue:
			# add the right child node to the end of the queue
			queue.append(right)
		# add the left child node to the end of the queue
		queue.append(left)
	# return the maximum value found
	return maxValue

# First Best
# We use a queue to keep track of the nodes in the search tree and explore the tree in a best-first manner.
# At each node, we calculate the bound value and prioritize the node with the highest bound value to be explored next.
# We add the node with the highest bound value to the front of the queue, and the other child node to the end of the queue.
# The method returns the maximum value found by exploring the tree.
def knapsack_first_best(wt, val, w): 
	# n is the number of items in the knapsack problem
	n = len(val) 
	# maxValue stores the maximum value that can be obtained by the knapsack problem
	maxValue = 0 
	# u is the capacity of the knapsack
	u = w 
	# node is the first node in the knapsack problem
	# the level is -1, the value is 0, the weight is 0, and the bound is 0
	node = Node(-1, 0, 0, 0) 
	# queue stores all the nodes in the knapsack problem
	queue = []
 
	# append the first node to the queue
	queue.append(node)
 
	# continue the loop as long as there is any node in the queue
	while len(queue) != 0: 
		# pop the first node in the queue and assign it to node
		node = queue.pop(0) 
		# if node level is equal to n-1, it means that all items have been processed
		# so we continue to the next iteration
		if node.level == n - 1: 
			continue
  
		# create the left node
		# level is node level + 1
		# value is node value + val[node level + 1]
		# weight is node weight + wt[node level + 1]
		# bound is 0
		left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0)
 
		# if the weight of the left node is less than or equal to the capacity of the knapsack and the value is greater than maxValue
		# update maxValue to the value of the left node
		if left.weight <= w and left.value > maxValue: 
			maxValue = left.value
 
		# create the right node
		# level is node level + 1
		# value is node value
		# weight is node weight
		# bound is 0
		right = Node(node.level + 1, node.value, node.weight, 0)
 
		# calculate the bound of the right node
		bound = boundValue(right, n, w, val, wt)
 
		# if the bound of the right node is greater than maxValue, append the right node to the queue
		if bound > maxValue: 
			queue.append(right)
 
		# if the bound of the right node is greater than or equal to maxValue, append the left node to the queue
		if bound >= maxValue: 
			queue.append(left)
 
	# return the maximum value that can be obtained by the knapsack problem
	return maxValue

def main():
	# Define the weight and value lists and the capacity of the knapsack
	weights = [10, 20, 30]
	values = [60, 100, 120]
	capacity = 50
	
	# Call each of the algorithms
	print("""Choosing the best algorithm for the 0/1 Knapsack problem depends on the specific requirements of the problem at hand.
  - Dynamic Programming is a general-purpose algorithm that is guaranteed to find the optimal solution in polynomial time, but it can be slow for larger problem sizes.
  - Divide and Conquer is a faster alternative to Dynamic Programming, but it may not always give the optimal solution.
  - Greedy Algorithm is a fast and simple algorithm that gives a good approximation of the optimal solution, but it may not always give the exact solution.
  - Branch and Bound algorithms, including First Depth, First Breadth, and First Best, can be more efficient than Dynamic Programming in certain cases, but they may also be slower in others.

Ultimately, the best algorithm to use depends on the size and nature of the problem, as well as the desired trade-off between accuracy and computational efficiency.
""")
	print("Dynamic Programming:", knapsack_dynamic(weights, values, capacity))

	print("Divide and Conquer:", knapsack_divide_conquer(weights, values, capacity))

	print("Greedy Algorithm:", knapsack_greedy(weights, values, capacity))

	print("Branch and Bound, First Depth:", knapsack_first_depth(weights, values, capacity))
	print("Branch and Bound, First Breadth:", knapsack_first_breadth(weights, values, capacity))
	print("Branch and Bound, First Best:", knapsack_first_best(weights, values, capacity))
	
if __name__ == '__main__':
	main()
