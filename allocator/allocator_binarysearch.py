import bisect
import time

class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = []  # 전체 arena
		self.in_use = {}  # id : (시작 주소, 크기)
		self.free_space = []  # free space (시작 주소, 크기)
		self.total_size = 0  # 현재까지 할당된 전체 메모리 크기

	def print_stats(self):
		in_use_size = sum(size for _, size in self.in_use.values())
		arena_size = len(self.arena) * self.chunk_size
		utilization = in_use_size / arena_size

		print(f"Arena: {arena_size / (1024 * 1024):.2f} MB")
		print(f"In-use: {in_use_size / (1024 * 1024):.2f} MB")
		print(f"Utilization: {utilization:.5f}")		# 유효숫자 맞추기

	def malloc(self, id, size):
		if size % self.chunk_size != 0:		# chunk 사이즈에 딱 떨어지지 않는 경우
			required_size = ((size // self.chunk_size) + 1) * self.chunk_size
		else:
			required_size = size

		# 적합한 크기의 chunk 할당		
		idx = bisect.bisect_left(self.free_space, (0, required_size))		# 정렬된 순서를 유지하도록 free space에 할당할 chunk를 삽입할 위치 찾기
		if idx < len(self.free_space) and self.free_space[idx][1] >= required_size:
			start, _ = self.free_space.pop(idx)
			self.in_use[id] = (start, required_size)
		else:
			start = self.total_size
			self.total_size += required_size
			self.arena.extend([0] * (required_size // self.chunk_size))
			self.in_use[id] = (start, required_size)

	def free(self, id):
		if id in self.in_use:
			start, size = self.in_use.pop(id)
			bisect.insort(self.free_space, (start, size))		# free space에 chunk를 chunk의 기존 항목 다음에 삽입
			self.merge()
		else:
			print("free: failed to free")

	def merge(self):		# 연속된 free space merge
		merged_list = []
        ## 이거 안됨.. 코드 고쳐야됨.. 바보 gpt도 못 고쳐줌ㅠ
		for start, size in sorted(self.free_space):        # 시작 포인터를 기준으로 정렬된 free_space 리스트를 사용
			if merged_list and merged_list[-1][0] + merged_list[-1][1] == start:
				merged_list[-1] = (merged_list[-1][0], merged_list[-1][1] + size)
			else:
				merged_list.append((start, size))
		self.free_space = merged_list

if __name__ == "__main__":
	allocator = Allocator()
	start = time.time()
	
	with open ("./allocator/input.txt", "r") as file:
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
	
	end = time.time()
	allocator.print_stats()
	print(f"{end - start :.3f}")