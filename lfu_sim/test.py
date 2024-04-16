# import time

class Min_Heap:
	def __init__(self, *args):
		if len(args) != 0:
			self.A = args[0]
		else:
			self.A = []
 
	def insert(self, x):
		self.A.append(x)
		self.percolateUp(len(self.A)-1)

	def percolateUp(self, i:int):
		parent = (i - 1) // 2
		if i > 0 and self.A[i] < self.A[parent]:
			self.A[i], self.A[parent] = self.A[parent], self.A[i]
			self.percolateUp(parent)

	def deleteMin(self):
		if (not self.isEmpty()):
			min = self.A[0]
			self.A[0] = self.A.pop()
			self.__percolateDown(0)
			return min
		else:
			return None

	def __percolateDown(self, i:int):
		child = 2 * i + 1  # left child
		right = 2 * i + 2  # right child
		if (child <= len(self.A)-1):
			if (right <= len(self.A)-1 and self.A[right] < self.A[child]):
				child = right
			if self.A[i] > self.A[child]:
				self.A[i], self.A[child] = self.A[child], self.A[i]
				self.__percolateDown(child)

	def min(self):
		return self.A[0]

	def isEmpty(self) -> bool:
		return len(self.A) == 0

	def clear(self):
		self.A = []

	def size(self) -> int:
		return len(self.A)

# lpn과 frequency를 모두 저장하는 class
class LFU_Node:
	def __init__(self, key, lpn, frequency=1):
		self.key = key
		self.lpn = lpn
		self.frequency = frequency
		# self.time = time.time()

	def __lt__(self, other):
		# if self.frequency == other.frequency:
		# 	return self.time < other.time # 빈도수가 같을 때, 오래 있었던 원소가 우선순위를 가질 수 있도록
		return self.frequency < other.frequency

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = Min_Heap()
        self.freq = {}

    def get(self, key):
        if key in self.freq:
            node = self.freq[key]
            node.frequency += 1
            self.cache.percolateUp(self.cache.A.index(node))  # 캐시에 존재하는 노드의 우선순위를 높임
            return node
        return None

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.freq:
            node = self.freq[key]
            node.value = value
            node.frequency += 1
            self.cache.percolateUp(node)  # 캐시에 존재하는 노드의 우선순위를 높임
        else:
            if len(self.freq) >= self.capacity:
                least_freq_node = self.cache.deleteMin()
                del self.freq[least_freq_node.key]

            node = LFU_Node(key, value)
            self.freq[key] = node
            self.cache.insert(node)

def lfu_sim(cache_slots):
	cache_hit = 0
	tot_cnt = 0
	cache = LFUCache(cache_slots)

	data_file = open("/Users/jisoo/ds24/ds24/lfu_sim/linkbench.trc")
	
	for line in data_file.readlines():
		lpn = line.split()[0] # 각 라인 출력
		tot_cnt += 1

		if cache.get(lpn) is not None:
			cache_hit += 1
		else:
			cache.put(lpn, lpn)

	print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit ratio = ", cache_hit / tot_cnt)
	
if __name__ == "__main__":
	for cache_slots in range(100, 1000, 100):
		lfu_sim(cache_slots)
