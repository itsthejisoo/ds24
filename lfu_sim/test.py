import time
import math

class Min_Heap:
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
		if i > 0 and self.__A[i] < self.__A[parent]:
			self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
			self.__percolateUp(parent)

	def deleteMin(self):
		if (not self.isEmpty()):
			min = self.__A[0]
			self.__A[0] = self.__A.pop()
			self.__percolateDown(0)
			return min
		else:
			return None

	def __percolateDown(self, i:int):
		child = 2 * i + 1  # left child
		right = 2 * i + 2  # right child
		if (child <= len(self.__A)-1):
			if (right <= len(self.__A)-1 and self.__A[right] < self.__A[child]):
				child = right
			if self.__A[i] > self.__A[child]:
				self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
				self.__percolateDown(child)

	def findIndex(self, node):
		for i, n in enumerate(self.__A): # 인덱스와 원소 동시 접근
			if n.lpn == node.lpn:
				return i
		return None

	def updateheap(self, node):
		idx = self.findIndex(node)
		if idx is not None:
			self.__A[idx] = node
			self.__percolateDown(idx)

	def min(self):
		return self.__A[0]

	def isEmpty(self) -> bool:
		return len(self.__A) == 0

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
					print(self.__A[i].lpn, self.__A[i].frequency, end=' ')
					i += 1
				if i == 2 ** k - 1:
					print('\n')
					k += 1
		print('\n=========================')


# lpn과 frequency를 모두 저장하는 class
class LFU_Node:
	def __init__(self, lpn, frequency:int):
		self.lpn = lpn
		self.frequency = frequency
		self.time = time.time()

	def __lt__(self, other):
		if self.frequency == other.frequency:
			return self.time < other.time # 빈도수가 같을 때, 오래 있었던 원소가 우선순위를 가질 수 있도록
		return self.frequency < other.frequency

def lfu_sim(cache_slots):
	cache_hit = 0
	tot_cnt = 0
	cache = {}
	heap = Min_Heap()

	data_file = open("lfu_sim/linkbench_test.trc")
	
	for line in data_file.readlines():
		lpn = line.split()[0] # 각 라인 출력
		tot_cnt += 1

		if lpn in cache:  # cache[lpn] : frequency
			cache[lpn] += 1
			cache_hit += 1
			node = LFU_Node(lpn, cache[lpn])
			heap.updateheap(node)
			heap.heapPrint()
		else:
			if len(cache) >= cache_slots:
				min_node = heap.deleteMin()
				del cache[min_node.lpn]
			cache[lpn] = 1
			new_node = LFU_Node(lpn, 1)
			heap.insert(new_node)
			heap.heapPrint()

	print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit ratio = ", cache_hit / tot_cnt)
	
if __name__ == "__main__":
	lfu_sim(10)
