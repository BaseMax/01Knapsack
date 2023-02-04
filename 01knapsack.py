# Dynamic Programming
def knapsack_dynamic(wt, val, w):
	n = len(val)
	K = [[0 for x in range(w + 1)] for x in range(n + 1)]
  
	for i in range(n + 1):
		for wt in range(w + 1):
			if i == 0 or wt == 0:
				K[i][wt] = 0
			elif wt >= wt[i-1]:
				K[i][wt] = max(val[i-1] + K[i-1][wt-wt[i-1]],  K[i-1][wt])
			else:
				K[i][wt] = K[i-1][wt]
  
	return K[n][w]

# Divide and Conquer
def knapsack_divide_conquer(wt, val, w):
	if w == 0 or len(wt) == 0:
		return 0
  
	if len(wt) == 1:
		if wt[0] <= w:
			return val[0]
		else:
			return 0
  
	return max(val[0] + knapsack_divide_conquer(wt[1:], val[1:], w-wt[0]), knapsack_divide_conquer(wt[1:], val[1:], w))

# Greedy Algorithm
def knapsack_greedy(wt, val, w):
	n = len(val)
	ratio = []
	for i in range(0,n):
		ratio.append(val[i]/wt[i])
  
	for i in range(0,n):
		for j in range(0,n - i - 1):
			if ratio[j] < ratio[j + 1]:
				ratio[j], ratio[j + 1] = ratio[j + 1], ratio[j]
				wt[j], wt[j + 1] = wt[j + 1], wt[j]
				val[j], val[j + 1] = val[j + 1], val[j]
  
	totalValue = 0
	for i in range(0,n):
		if wt[i] <= w:
			totalValue += val[i]
			w -= wt[i]
		else:
			break
	return totalValue 

# Branch and Bound
class Node:
	def __init__(self, level, value, weight, bound):
		self.level = level 
		self.value = value 
		self.weight = weight 
		self.bound = bound 

def boundValue(node, n, w, val, wt): 
    if node.weight >= w: 
        return 0
  
    bound = node.value 
    j = node.level + 1
    totalWeight = node.weight 
  
    while (j < n and totalWeight + wt[j] <= w): 
        totalWeight += wt[j] 
        bound += val[j] 
        j += 1
  
    if j < n: 
        bound += (w - totalWeight) * val[j]/wt[j] 
  
    return bound 

# First Depth
def knapsack_first_depth(wt, val, w): 
    n = len(val) 
    maxValue = 0 
    u = w 
    node = Node(-1, 0, 0, 0) 
    stack = [] 
  
    stack.append(node) 
  
    while(len(stack) != 0): 
        node = stack.pop() 
        if node.level == n - 1: 
            continue
  
        left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0) 
  
        if left.weight <= w and left.value > maxValue: 
            maxValue = left.value 
  
        right = Node(node.level + 1, node.value, node.weight, 0) 
  
        bound = boundValue(right, n, w, val, wt) 
  
        if bound > maxValue: 
            stack.append(right) 
  
        stack.append(left) 
  
    return maxValue

# First Breadth
def knapsack_first_breadth(wt, val, w): 
    n = len(val) 
    maxValue = 0 
    u = w 
    node = Node(-1, 0, 0, 0) 
    queue = [] 
  
    queue.append(node) 
  
    while(len(queue) != 0): 
        node = queue.pop(0) 
        if node.level == n - 1: 
            continue
  
        left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0) 
  
        if left.weight <= w and left.value > maxValue: 
            maxValue = left.value 
  
        right = Node(node.level + 1, node.value, node.weight, 0) 
        bound = boundValue(right, n, w, val, wt) 
  
        if bound > maxValue: 
            queue.append(right) 
  
        queue.append(left) 
  
    return maxValue 

# First Best
def knapsack_first_best(wt, val, w): 
    n = len(val) 
    maxValue = 0 
    u = w 
    node = Node(-1, 0, 0, 0) 
    queue = [] 
  
    queue.append(node) 
  
    while(len(queue) != 0): 
        node = queue.pop(0) 
        if node.level == n - 1: 
            continue
  
        left = Node(node.level + 1, node.value + val[node.level + 1], node.weight + wt[node.level + 1], 0) 
  
        if left.weight <= w and left.value > maxValue: 
            maxValue = left.value 
  
        right = Node(node.level + 1, node.value, node.weight, 0) 
  
        bound = boundValue(right, n, w, val, wt) 
  
        if bound > maxValue: 
            queue.append(right) 
  
        if bound >= maxValue: 
            queue.append(left) 
  
    return maxValue 

def main():
	# Define the weight and value lists and the capacity of the knapsack
	wt = [10, 20, 30]
	val = [60, 100, 120]
	w = 50
	
	# Call each of the algorithms
	print("Dynamic Programming:", knapsack_dynamic(wt, val, w))
	print("Divide and Conquer:", knapsack_divide_conquer(wt, val, w))
	print("Greedy Algorithm:", knapsack_greedy(wt, val, w))
	print("Branch and Bound, First Depth:", knapsack_first_depth(wt, val, w))
	print("Branch and Bound, First Breadth:", knapsack_first_breadth(wt, val, w))
	print("Branch and Bound, First Best:", knapsack_first_best(wt, val, w))
	
if __name__ == '__main__':
	main()
