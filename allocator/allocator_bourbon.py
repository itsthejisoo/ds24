class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = {}          # chunk를 저장하는 리스트
		self.ac_num = 0  		 # 아레나 안에 있는 청크 총 개수
		self.free_space = 0      # free한 chunk 개수
		self.in_use_size = 0     # 사용 중인 메모리 크기

	def print_stats(self):
		arena_size = len(self.arena) * self.chunk_size
		utilization = self.in_use_size / arena_size if arena_size > 0 else 0

		print("Arena: ", arena_size // (1024 * 1024), "MB")
		print("In-use: ", self.in_use_size // (1024 * 1024), "MB")
		print("Utilization: {:.3f}".format(utilization))

	def malloc(self, id, size):
		chunk_num = (size + self.chunk_size - 1) // self.chunk_size

		if self.free_space >= chunk_num:  	# free 청크가 충분한 경우
			self.free_space -= chunk_num
		else:  								# free 청크가 충분하지 않은 경우
			chunk_num -= self.free_space
			self.ac_num += chunk_num
			self.free_space = 0

		self.arena[id] = (size, chunk_num)
		self.in_use_size += size

	def free(self, id):
		if id in self.arena:
			size, chunk_num = self.arena.pop(id)
			self.free_space += chunk_num
			self.in_use_size -= size
		else:
			print("free: No such ID in arena list")
			return

if __name__ == "__main__":
	allocator = Allocator()

	with open("allocator/input.txt", "r") as file:
		n = 0
		for line in file:
			req = line.split()
			if req[0] == 'a':
				allocator.malloc(int(req[1]), int(req[2]))
			elif req[0] == 'f':
				allocator.free(int(req[1]))
			
			# if n%100 == 0:
			#     print(n, "...")

			n += 1

	allocator.print_stats()