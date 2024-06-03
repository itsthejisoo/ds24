'''잘못 짰음ㅠ'''
'''
class Node:
	def __init__(self, size):
		self.size = size
		self.next = None

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

	# chunk 사이즈에 맞게 해시테이블 노드 할당하기
	def node_list(self, size, tNode: Node, n: int):
		c_n = (size // self.chunk_size) + 1  # 청크 개수
		if n == 1:
			tNode.next = Node(size - c_n * self.chunk_size)  # 마지막 청크의 크기 조정
		else:
			tNode.next = Node(self.chunk_size)  # 중간 청크는 고정 크기
		n -= 1
		if n != 0:
			self.node_list(size, tNode.next, n)  # 재귀적으로 노드 연결

	def malloc(self, id, size):  # O(n)
		# 할당해야 할 청크 개수 계산
		chunk_num = (size // self.chunk_size) + 1

		# Free space에서 필요한 청크를 할당
		if self.free_space >= chunk_num:
			self.free_space -= chunk_num  # free space에서 청크를 가져옴
		else:
			new_chunks = chunk_num - self.free_space
			self.arean_chunk_num += new_chunks  # 부족한 만큼 새로운 청크 추가
			self.free_space = 0

		if chunk_num > 1:  # chunk 개수가 2개 이상일 때
			new_node = Node(self.chunk_size)
			self.node_list(size, new_node, chunk_num - 1)
		else:  # chunk 개수가 1개일 때
			new_node = Node(size)

		if self.arena[id] is None:  # 메모리 안의 청크가 비어있을 때
			self.arena[id] = new_node
		else:  # 메모리 안의 청크가 이미 할당된 경우, 끝에 연결 // input.txt한에선 이런 경우는 없음 -> O(1)
			curr = self.arena[id]
			while curr.next:
				curr = curr.next
			curr.next = new_node

		self.in_use_size += size  # 사용 중인 메모리 크기 업데이트

	def free(self, id):  # O(n)
		curr = self.arena[id]

		if curr is None:
			print("free: No such ID in hash table")
			return

		chunk_count = 0
		while curr:  # in_use 사이즈 업데이트 및 chunk 개수 계산
			self.in_use_size -= curr.size
			chunk_count += 1
			curr = curr.next

		self.free_space += chunk_count  # free space에 청크 추가
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
'''