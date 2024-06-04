import time

class Allocator:
	def __init__(self):
		self.chunk_size = 4096  
		self.arena = []  # 전체 메모리 풀을 관리하는 리스트
		self.in_use = {}  # 사용 중인 메모리를 저장하는 딕셔너리
		self.free_space = {self.chunk_size: []}  # 사용 가능한 공간을 관리하는 딕셔너리
		
	def print_stats(self):
		# 메모리 풀 크기, 사용 중인 메모리 크기, 이용률을 출력
		arena_size_mb = len(self.arena) * (self.chunk_size / 1024 / 1024)
		in_use_size_mb = sum(size for size, _ in self.in_use.values()) / 1024 / 1024
		utilization = in_use_size_mb / arena_size_mb

		print(f"Arena: {arena_size_mb:.2f} MB")
		print(f"In-use: {in_use_size_mb:.2f} MB")
		print(f"Utilization: {utilization:.5f}")

	def malloc(self, id, size):
		numpowerof2 = 1		# 요청한 크기보다 큰 2의 거듭제곱 중 가장 작은 값을 찾음

		while numpowerof2 < size:
			numpowerof2 *= 2
		
		if numpowerof2 > self.chunk_size:
			print("malloc: request size is bigger than chunk size")
		
		# 사용 가능한 청크를 찾음
		if numpowerof2 in self.free_space and self.free_space[numpowerof2]:
			address = self.free_space[numpowerof2].pop()
		else:
			address = self.allocate_from_OS(numpowerof2)
		
		self.in_use[id] = (numpowerof2, address)  # 할당된 메모리를 in_use에 저장
	
	def free(self, id):
		if id in self.in_use:
			chunk_size, address = self.in_use.pop(id)  # 사용 중인 메모리에서 제거
			self.coalescing(chunk_size, address)  # 해제된 메모리를 처리
		else:
			print(f"free: ID invalid")

	def allocate_from_OS(self, chunk_size):		# OS로부터 새로운 청크를 할당
		current_size = self.chunk_size
		address = len(self.arena)
		
		while current_size > chunk_size:
			buddy_size = current_size // 2
			if buddy_size not in self.free_space:
				self.free_space[buddy_size] = []
			self.free_space[buddy_size].append(address + buddy_size // self.chunk_size)
			current_size //= 2
		
		self.arena.append(chunk_size)
		return address

	def coalescing(self, chunk_size, address):        # 청크를 해제하고, 연속된 free chunk가 있으면 병합
		while chunk_size < self.chunk_size:
			buddy_address = address ^ chunk_size
			
			if buddy_address in self.free_space[chunk_size]:
				self.free_space[chunk_size].remove(buddy_address)
				address = min(address, buddy_address)
				chunk_size *= 2
			else:
				break
		
		if chunk_size not in self.free_space:
			self.free_space[chunk_size] = []
		self.free_space[chunk_size].append(address)  # 해제된 청크를 free space에 추가


if __name__ == "__main__":
	allocator = Allocator()
	start = time.time()
	
	with open ("allocator/input.txt", "r") as file:
		n = 0
		for line in file:
			req = line.split()
			if req[0] == 'a':  # 메모리 할당 요청
				allocator.malloc(int(req[1]), int(req[2]))
			elif req[0] == 'f':  # 메모리 해제 요청
				allocator.free(int(req[1]))

			# if n % 100 == 0:
			#     print(n, "...")
			
			n += 1
	
	end = time.time()
	allocator.print_stats()
	print(f"time: {end - start: .3f}")