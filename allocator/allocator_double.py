class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = [None] * 1024 * 1024
		self.in_use_size = 0  # 사용 중인 메모리 크기
		self.arean_chunk_num = 0  # 아레나 안에 있는 청크 총 개수
		self.free_space = 0  # 사용 가능한 free space 청크 개수

	def print_stats(self):
		arena_size = self.arean_chunk_num * self.chunk_size
		utilization = self.in_use_size / arena_size

		# MB 단위로 변환하여 출력
		print("Arena: ", arena_size // (1024 * 1024), "MB")  		# 유효숫자 맞춰주기 위해서 '//' 사용함. 실제로 390.71875... 나옴
		print("In-use: ", self.in_use_size // (1024 * 1024), "MB")  # 이하 동문. 실제로 162.18604...나옴
		print("Utilization: {:.3f}".format(utilization))  			# 유효숫자 맞추기 위해 3번째 소수점까지

	def malloc(self, id, size):  # O(n)
		# 할당해야 할 청크 개수 계산
		chunk_num = (size // self.chunk_size) + 1
		if self.arena[id] is None:  # 메모리 안의 청크가 비어있을 때
			# Free space에서 필요한 청크를 할당
			if self.free_space >= chunk_num:
				self.free_space -= chunk_num  # free space에서 청크를 가져옴
			else:
				new_chunks = chunk_num - self.free_space
				self.arean_chunk_num += new_chunks  # 부족한 만큼 새로운 청크 추가
				self.free_space = 0

			if chunk_num > 1:  # chunk 개수가 2개 이상일 때
				new_list = [self.chunk_size] * (chunk_num-1)
				new_list.append(size - (self.chunk_size * (chunk_num - 1)))
			else:  # chunk 개수가 1개일 때
				new_list = [size]
			self.arena[id] = new_list

		else:  # 메모리 안의 청크가 이미 할당된 경우, 끝에 연결 // input.txt한에선 이런 경우는 없음 -> O(1)
			id_endsize = self.arena[id][len(self.arena[id]) - 1]
			if id_endsize < self.chunk_size:
				self.arena[id].append(size - (self.chunk_size - id_endsize))
				self.arena[id][len(self.arena[id]) - 1] = self.chunk_size
			else:
				if self.free_space >= chunk_num:
					self.free_space -= chunk_num  # free space에서 청크를 가져옴
				else:
					new_chunks = chunk_num - self.free_space
					self.arean_chunk_num += new_chunks  # 부족한 만큼 새로운 청크 추가
					self.free_space = 0

				if chunk_num > 1:  # chunk 개수가 2개 이상일 때
					new_list = [self.chunk_size] * (chunk_num-1)
					new_list.append(size - (self.chunk_size * (chunk_num - 1)))
				else:  # chunk 개수가 1개일 때
					new_list = [size]
		self.in_use_size += size  # 사용 중인 메모리 크기 업데이트

	def free(self, id):  # O(n)
		if self.arena[id] is None:
			print("free: No such ID in hash table")
			return

		self.free_space += len(self.arena[id])  # free space에 청크 추가
		self.in_use_size -= sum(self.arena[id]) # -> O(n)
		self.arena[id] = None  # 해당 ID의 청크 모두 삭제

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