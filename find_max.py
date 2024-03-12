num = [2, 4, 1, 8, 9, 3]

def find_max_recursive(num, n):
	if n == 1:
		return num[0]
	else:
		return num[0] if num[0] > find_max_recursive(num[1:], n - 1) else find_max_recursive(num[1:], n - 1)

def find_max_iterative(num):
	max = num[0]
	for i in range(len(num)):
		if num[i] > max:
			max = num[i]
		else:
			continue
	return max

print("recursive method: ", find_max_recursive(num, len(num) - 1))
print("iterative method: ", find_max_iterative(num))
