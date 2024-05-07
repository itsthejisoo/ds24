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

	def findIndex(self, lpn) -> int:
		for i, n in enumerate(self.__A):
			if n.lpn == lpn:
				return i
		return False

	def updateheap(self, i:int, point:int):
		if i >= 0:
			self.__A[i].frequency += 1
			self.__A[i].point = point
			self.__percolateDown(i)

	def min(self):
		return self.__A[0]

	def isEmpty(self) -> bool:
		return len(self.__A) == 0

	def size(self) -> int:
		return len(self.__A)

# lpn과 frequency 모두 저장하는 클래스
class LFU_Node:
	def __init__(self, lpn, frequency):
		self.lpn = lpn
		self.frequency = frequency
		self.point = 0
	
	def __lt__(self, other):
		if self.frequency == other.frequency:	# 빈도수가 같을 때, 먼저 들어온 원소에게 높은 우선순위 줌
			return self.point < other.point
		return self.frequency < other.frequency
	
def lfu_sim(cache_slots):
	cache_hit = 0
	tot_cnt = 0
	cache_heap = Min_Heap()
	cache = {}

	data_file = open("lfu_sim/linkbench.trc")

	for line in data_file.readlines():
		lpn = line.split()[0]					# 한 줄씩 원소를 불러옴
		tot_cnt += 1

		if cache_heap.findIndex(lpn) is False:		# cache힙에 없을때
			if cache_heap.size() == cache_slots:	# cache가 가득 찼을 때, 빈도수가 작은 원소를 삭제시킴
				cache_heap.deleteMin()
			if lpn in cache:					# 캐시 삭제와 상관없이 frequency 저장
				cache[lpn] += 1
			else:
				cache[lpn] = 1
			newnode = LFU_Node(lpn, cache[lpn])
			newnode.point = tot_cnt				# 언제 들어왔는지
			cache_heap.insert(newnode)
		else:									# cache안에 lpn이 있을때(hit)
			cache[lpn] += 1
			cache_hit += 1
			i = cache_heap.findIndex(lpn)
			cache_heap.updateheap(i, tot_cnt)	# frequency, point 업데이트

	print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit ratio = ", cache_hit / tot_cnt)

if __name__ == "__main__":
	for cache_slots in range(100, 1000, 100):
		lfu_sim(cache_slots)

# 배열이 아니라 리스튼데 오버플로우가 될 수 있나?
# 리스트는 배열이랑 다르게 크기 변환이 가능한걸로 알고 있는데? -> question