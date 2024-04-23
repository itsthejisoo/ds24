def shellSort(A):
	H = gapSequence(len(A))
	for h in H:
		for k in range(h):
			stepInsertionSort(A, k, h)

def stepInsertionSort(A, k:int, h:int): # 갭이 h일때
	for i in range(k + h, len(A), h):
		j = i - h
		newItem = A[i]
		while j >= 0 and newItem < A[j]:
			A[j + h] = A[j]
			j -= h
		A[j + h] = newItem

def gapSequence(n:int) -> list:
	H = [1]; gap = 1
	while gap < n/5:
		gap = 3 * gap + 1
		H.append(gap)
	H.reverse()
	return H

'''def shellSort_1(A):
	gap = 1
	while gap < len(A) // 3:
		gap = 3 * gap + 1
	
	while gap >= 1:
		for i in range(gap, len(A)):
			newItem = A[i]
			loc = i
			while loc >= gap and A[loc - gap] > newItem:
				A[loc] = A[loc - gap]
				loc -= gap
			A[loc] = newItem
		gap //= 3
	
	return A'''

# def shellSort(arr):
#     n = len(arr)
#     gap = 1
#     while gap < n // 3:
#         gap = gap * 3 + 1  # Sedgewick gap sequence

#     while gap >= 1:
#         for i in range(gap, n):
#             temp = arr[i]
#             j = i
#             while j >= gap and arr[j - gap] > temp:
#                 arr[j] = arr[j - gap]
#                 j -= gap
#             arr[j] = temp
#         gap //= 3
#     return arr 