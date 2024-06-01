class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = {}
		self.in_use_size = 0	 # 사용 중인 메모리 크기
		self.ac_num = 0			# arena 안에 있는 청크 총 개수
		self.free_chunks = 0	 # 사용 가능한 free space 청크 개수

	def print_stats(self):
		arena_size = self.ac_num * self.chunk_size
		utilization = self.in_use_size / arena_size

		print("Arena: ", arena_size // (1024 * 1024), "MB")  		# 유효숫자 맞춰주기 위해서 '//' 사용함. 실제로 390.71875... 나옴
		print("In-use: ", self.in_use_size // (1024 * 1024), "MB")  # 이하 동문. 실제로 162.18604...나옴
		print("Utilization: {:.3f}".format(utilization))  			# 유효숫자 맞추기 위해 3번째 소수점까지

	def malloc(self, id, size):  # 할당해야할 청크 개수 구하고 딕셔너리에 추가하기
		chunk_num = (size // self.chunk_size) + 1

		# Free space에서 필요한 청크를 할당
		allocated_chunks = []
		remaining_size = size

		if self.free_chunks >= chunk_num:	# free 청크가 충분한 경우
			self.free_chunks -= chunk_num
		else:								# free 청크가 충분하지 않은 경우
			chunk_num -= self.free_chunks
			self.free_chunks = 0
			self.ac_num += chunk_num

		while remaining_size > self.chunk_size:
			allocated_chunks.append(self.chunk_size)
			remaining_size -= self.chunk_size

		allocated_chunks.append(remaining_size)

		if id in self.arena:  	# arena에 이미 id가 존재하고 추가로 chunk 할당할 경우
			self.arena[id].extend(allocated_chunks)
		else:  					# 새로운 id에 메모리 할당할 경우
			self.arena[id] = allocated_chunks

		self.in_use_size += size

	def free(self, id):
		if id not in self.arena:
			print("free: No such ID in hash table")
			return

		free_chunks = self.arena[id]
		chunk_count = len(free_chunks)

		self.free_chunks += chunk_count
		self.in_use_size -= sum(free_chunks)
		del self.arena[id]

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