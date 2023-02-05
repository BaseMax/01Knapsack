# Dynamic Programming
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
				K[i][c] = max(values[i-1] + K[i-1][c-weights[i-1]], K[i-1][c])
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
	# append the node to the stack
	stack.append(node)
	# keep looping until the stack is empty
	while len(stack) != 0:
		# pop the last node from the stack
		node = stack.pop()
		# increment the level of the node
		node.level += 1
		# if the level of the node is less than the number of items
		if node.level < n:
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 0
			leftNode = Node(node.level, node.value, node.weight, 0)
			# add the value of the current item to the value of the left node
			leftNode.value += val[leftNode.level]
			# add the weight of the current item to the weight of the left node
			leftNode.weight += wt[leftNode.level]
			# if the weight of the left node is less than or equal to the maximum weight and the value of the left node is greater than the maximum value found so far
			if leftNode.weight <= w and leftNode.value > maxValue:
				# update the maximum value found so far
				maxValue = leftNode.value
			# calculate the bound value of the left node
			leftNode.bound = boundValue(leftNode, n, w, val, wt)
			# if the bound value of the left node is greater than the maximum value found so far
			if leftNode.bound > maxValue:
				# append the left node to the stack
				stack.append(leftNode)
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 1
			rightNode = Node(node.level, node.value, node.weight, 1)
			# calculate the bound value of the right node
			rightNode.bound = boundValue(rightNode, n, w, val, wt)
			# if the bound value of the right node is greater than the maximum value found so far
			if rightNode.bound > maxValue:
				# append the right node to the stack
				stack.append(rightNode)
	# return the maximum value found so far
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
		# pop the first node from the queue
		node = queue.pop(0)
		# increment the level of the node
		node.level += 1
		# if the level of the node is less than the number of items
		if node.level < n:
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 0
			leftNode = Node(node.level, node.value, node.weight, 0)
			# add the value of the current item to the value of the left node
			leftNode.value += val[leftNode.level]
			# add the weight of the current item to the weight of the left node
			leftNode.weight += wt[leftNode.level]
			# if the weight of the left node is less than or equal to the maximum weight and the value of the left node is greater than the maximum value found so far
			if leftNode.weight <= w and leftNode.value > maxValue:
				# update the maximum value found so far
				maxValue = leftNode.value
			# calculate the bound value of the left node
			leftNode.bound = boundValue(leftNode, n, w, val, wt)
			# if the bound value of the left node is greater than the maximum value found so far
			if leftNode.bound > maxValue:
				# append the left node to the queue
				queue.append(leftNode)
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 1
			rightNode = Node(node.level, node.value, node.weight, 1)
			# calculate the bound value of the right node
			rightNode.bound = boundValue(rightNode, n, w, val, wt)
			# if the bound value of the right node is greater than the maximum value found so far
			if rightNode.bound > maxValue:
				# append the right node to the queue
				queue.append(rightNode)
	# return the maximum value found so far
	return maxValue

# First Best
# We use a queue to keep track of the nodes in the search tree and explore the tree in a best-first manner.
# At each node, we calculate the bound value and prioritize the node with the highest bound value to be explored next.
# We add the node with the highest bound value to the front of the queue, and the other child node to the end of the queue.
# The method returns the maximum value found by exploring the tree.
def knapsack_first_best(wt, val, w):
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
		# pop the first node from the queue
		node = queue.pop(0)
		# increment the level of the node
		node.level += 1
		# if the level of the node is less than the number of items
		if node.level < n:
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 0
			leftNode = Node(node.level, node.value, node.weight, 0)
			# add the value of the current item to the value of the left node
			leftNode.value += val[leftNode.level]
			# add the weight of the current item to the weight of the left node
			leftNode.weight += wt[leftNode.level]
			# if the weight of the left node is less than or equal to the maximum weight and the value of the left node is greater than the maximum value found so far
			if leftNode.weight <= w and leftNode.value > maxValue:
				# update the maximum value found so far
				maxValue = leftNode.value
			# calculate the bound value of the left node
			leftNode.bound = boundValue(leftNode, n, w, val, wt)
			# if the bound value of the left node is greater than the maximum value found so far
			if leftNode.bound > maxValue:
				# append the left node to the queue
				queue.append(leftNode)
			# create a new node with level equal to the level of the current node, value equal to the value of the current node, weight equal to the weight of the current node, and flag equal to 1
			rightNode = Node(node.level, node.value, node.weight, 1)
			# calculate the bound value of the right node
			rightNode.bound = boundValue(rightNode, n, w, val, wt)
			# if the bound value of the right node is greater than the maximum value found so far
			if rightNode.bound > maxValue:
				# append the right node to the queue
				queue.append(rightNode)
	# return the maximum value found so far
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
