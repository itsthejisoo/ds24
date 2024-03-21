from list.linkedListBasic import *
# 오래 걸리는데 돌아가긴 해요ㅠㅠ..

class CacheSimulator:
	def __init__(self, cache_slots):
		self.cache_slots = cache_slots
		self.cache_hit = 0
		self.tot_cnt = 1
		self.list = LinkedList()
	
	def do_sim(self, page):
		if(self.list.size() < cache_slots):
			for i in range(self.list.size()):
				if self.list.get(i) == page:
					self.list.remove(page)
					self.cache_hit += 1
			self.list.append(page)
			self.tot_cnt += 1
		else:
			for i in range(self.list.size()):
				if self.list.get(i) == page:
					self.list.remove(page)
					self.cache_hit += 1
			if self.list.size() > self.cache_slots - 1:
				self.list.pop(0)
			self.list.append(page)
			self.tot_cnt += 1

	def print_stats(self):
			print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":

	data_file = open(".\linkbench.trc")
	lines = data_file.readlines()
	for cache_slots in range(100, 1001, 100):
		cache_sim = CacheSimulator(cache_slots)
		for line in lines:
			page = line.split()[0]
			cache_sim.do_sim(page)
		
		cache_sim.print_stats()