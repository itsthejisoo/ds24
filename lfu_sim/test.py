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
		if (child < len(self.__A)):
			if (right < len(self.__A) and self.__A[right] < self.__A[child]):
				child = right
			if self.__A[i] > self.__A[child]:
				self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
				self.__percolateDown(child)
	
	def inHeap(self, lpn):
		for i, n in enumerate(self.__A):
			if n.lpn == lpn:
				return True

	def findIndex(self, lpn) -> int:
		for i, n in enumerate(self.__A):
			if n.lpn == lpn:
				return i

	def updateheap(self, i):
		if i >= 0:
			self.__A[i].frequency += 1
			self.__percolateDown(i)

	def min(self):
		return self.__A[0]

	def isEmpty(self) -> bool:
		return len(self.__A) == 0

	def size(self) -> int:
		return len(self.__A)

class LFU_Node:
	def __init__(self, lpn, frequency):
		self.lpn = lpn
		self.frequency = frequency
		self.point = 0
	
	def __lt__(self, other):
		if self.frequency == other.frequency:
			return self.point < other.point
		return self.frequency < other.frequency
	
def lfu_sim(cache_slots):
	cache_hit = 0
	tot_cnt = 0
	cache_heap = Min_Heap()
	cache = {}

	data_file = open("lfu_sim/linkbench.trc")

	for line in data_file.readlines():
		lpn = line.split()[0]
		tot_cnt += 1

		if not cache_heap.inHeap(lpn):
			if cache_heap.size() == cache_slots:
				cache_heap.deleteMin()
			if lpn in cache:
				cache[lpn] += 1
			else:
				cache[lpn] = 1
			newnode = LFU_Node(lpn, 1)
			newnode.point = tot_cnt
			cache_heap.insert(newnode)
		else:
			cache[lpn] += 1
			cache_hit += 1
			i = cache_heap.findIndex(lpn)
			cache_heap.updateheap(i)

	print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit ratio = ", cache_hit / tot_cnt)

if __name__ == "__main__":
	for cache_slots in range(100, 1000, 100):
		lfu_sim(cache_slots)