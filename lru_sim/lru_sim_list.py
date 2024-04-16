from list.linkedListBasic import *

class CacheSimulator:
	def __init__(self, cache_slots):
		self.cache_slots = cache_slots
		self.cache_hit = 0
		self.tot_cnt = 1
		self.lists = LinkedList()

	def do_sim(self, page):
		if self.lists.isEmpty():
			self.lists.append(page)
		else:
			if self.lists.size() >= cache_slots:
				if(self.lists.inNode(page)):
					self.lists.remove(page)
					self.cache_hit += 1
				else:
					self.lists.pop(0)
				self.lists.append(page)
				self.tot_cnt += 1
			else:
				if self.lists.inNode(page):
					self.lists.remove(page)
					self.cache_hit += 1
				self.lists.append(page)
				self.tot_cnt += 1

	def print_stats(self):
			print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)

if __name__ == "__main__":

	data_file = open("lru_sim/linkbench.trc")
	lines = data_file.readlines()
	for cache_slots in range(100, 1001, 100):
		cache_sim = CacheSimulator(cache_slots)
		for line in lines:
			page = line.split()[0]
			cache_sim.do_sim(page)
		
		cache_sim.print_stats()
