class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = {}
		self.in_use_size = 0	 			# 사용 중인 메모리 크기
		self.arena_chunk_num = 0			# arena 안에 있는 청크 총 개수 (arena 안에 있는 value를 sum 해서 계산해도 되지만 순회를 하게 되면 시간 복잡도가 떨어지기 떄문에 따로 추적하게 했음)
		self.free_space = 0					# 사용 가능한 free space 청크 개수

	def print_stats(self):
		arena_size = self.arena_chunk_num * self.chunk_size
		utilization = self.in_use_size / arena_size

		print("Arena: ", arena_size // (1024 * 1024), "MB")  		# 유효숫자 맞춰주기 위해서 '//' 사용함. 실제로 390.71875... 나옴
		print("In-use: ", self.in_use_size // (1024 * 1024), "MB")  # 이하 동문. 실제로 162.18604...나옴
		print("Utilization: {:.3f}".format(utilization))  			# 유효숫자 맞추기 위해 3번째 소수점까지

	def malloc(self, id, size):
		chunk_num = (size + self.chunk_size - 1) // self.chunk_size

		if self.free_space >= chunk_num:  	# free 청크가 충분한 경우
			self.free_space -= chunk_num
		else:  								# free 청크가 충분하지 않은 경우
			chunk_num -= self.free_space
			self.arena_chunk_num += chunk_num
			self.free_space = 0

		if id not in self.arena:		# arena에 id값인 메모리가 처음으로 할당하는 경우
			self.arena[id] = (size, chunk_num)
			self.in_use_size += size
		else:								# arena에 id값인 메모리가 이미 할당 되어 있는 경우
			self.arena[id][0] += size
			self.arena[id][1] += chunk_num

	def free(self, id):
		if id in self.arena:
			size, chunk_num = self.arena[id]
			self.arena[id] = (None, None)
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