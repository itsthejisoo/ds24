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
 
	def updateheap(self, lpn):
		for i, n in enumerate(self.__A): # 인덱스와 원소 동시 접근
			if n.lpn == lpn:
				n.frequency += 1
				self.__percolateDown(i)
				break

	def min(self):
		return self.__A[0]

	def isEmpty(self) -> bool:
		return len(self.__A) == 0

	def size(self) -> int:
		return len(self.__A)

# lpn과 frequency를 모두 저장하는 class
class LFU_Node:
	def __init__(self, lpn, frequency:int):
		self.lpn = lpn
		self.frequency = frequency
		self.point = 0 # 몇번째에 들어가는지 저장

	def __lt__(self, other):
		if self.frequency == other.frequency: # 빈도수가 같을 때, 오래된 원소에게 더 높은 우선순위를 준다.
			return self.point < other.point
		return self.frequency < other.frequency

def lfu_sim(cache_slots):
	cache_hit = 0
	tot_cnt = 0
	cache = {}
	storage = {} # cache와 상관없이 frequency 저장하는 딕셔너리
	heap = Min_Heap()

	data_file = open("lfu_sim/linkbench.trc")
	
	for line in data_file.readlines():
		lpn = line.split()[0] # 각 라인 출력
		tot_cnt += 1

		if lpn in cache:  # cache[lpn] : frequency
			cache[lpn] += 1; storage[lpn] += 1
			cache_hit += 1
			heap.updateheap(lpn)
		else:
			if heap.size() >= cache_slots:
				min_node = heap.deleteMin()
				del cache[min_node.lpn]
			cache[lpn] = 1; storage[lpn] = 1
			new_node = LFU_Node(lpn, 1)
			new_node.point = tot_cnt
			heap.insert(new_node)

	print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit ratio = ", cache_hit / tot_cnt)
	
if __name__ == "__main__":
	for cache_slots in range(100, 1000, 100):
		lfu_sim(cache_slots)
