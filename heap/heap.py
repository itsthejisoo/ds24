import math

class Heap:
	def __init__(self, *args):
		if len(args) != 0:
			self.__A = args[0] 
		else:
			self.__A = []
 
	def insert(self, x):
		self.__A.append(x)
		self.__percolateUp(len(self.__A)-1)

	def __percolateUp(self, i:int):
		parent = (i - 1) // 2
		if i > 0 and self.__A[i] > self.__A[parent]:
			self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
			self.__percolateUp(parent)

	def deleteMax(self):
		if (not self.isEmpty()):
			max = self.__A[0]
			self.__A[0] = self.__A.pop()
			self.__percolateDown(0)
			return max
		else:
			return None

	def __percolateDown(self, i:int):
		child = 2 * i + 1  # left child
		right = 2 * i + 2  # right child
		if (child <= len(self.__A)-1): # 얘도 까먹지마라
			if (right <= len(self.__A)-1 and self.__A[child] < self.__A[right]):
				child = right
			if self.__A[i] < self.__A[child]:
				self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
				self.__percolateDown(child)

	def max(self):
		return self.__A[0]

	def buildHeap(self):
		for i in range((len(self.__A) - 2) // 2, -1, -1):
			self.__percolateDown(i)

	def isEmpty(self) -> bool:
		# return len(self.__A) == 0
		return not bool(self.__A)

	def clear(self):
		self.__A = []

	def size(self) -> int:
		return len(self.__A)
	
	def height(self):
		return math.log2(self.size() + 1)
	
	def heapPrint(self):
		if self.isEmpty():
			print("Nothing in Heap\n")
		k = 1
		while k <= self.height():
			i = 2 ** (k - 1)
			for i in range(len(self.__A)):
				if i <= (2 ** k) - 2:
					print(self.__A[i], end=' ')
					i += 1
				if i == 2 ** k - 1:
					print('\n')
					k += 1
		print('\n=========================')
