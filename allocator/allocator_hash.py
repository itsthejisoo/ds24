class Node:
	def __init__(self, size):
		self.size = size
		self.next = None

class Allocator:
	def __init__(self):
		self.chunk_size = 4096
		self.arena = [None] * 1024 * 1024
		self.in_use_size = 0	# 사용 중인 메모리 크기
		self.ac_num = 0			# 아레나 안에 있는 청크 총 개수

	def print_stats(self):
		arena_size = self.ac_num * self.chunk_size
		utilization = self.in_use_size / arena_size if arena_size > 0 else 0

		# MB단위이므로 1M 나누기
		print("Arena: ", arena_size // (1024 * 1024), "MB")
		print("In-use: ", self.in_use_size // (1024 * 1024), "MB")
		print("Utilization: {:.3f}".format(utilization))
	
	# chunk 사이즈에 맞게 해시테이블 노드 할당하기
	def node_list(self, size, tNode:Node, n:int):
		c_n = (size // self.chunk_size) + 1		# 청크 개수
		if n == 1:
			tNode.next = Node(size - c_n * self.chunk_size)
		else:
			tNode.next = Node(self.chunk_size)
		n -= 1
		if n != 0:
			self.node_list(tNode.next, n)

	def malloc(self, id, size):		# O(n)
		# 할당해야할 청크 개수 구하고 해시 테이블 체인에 연결하기
		chunk_num = (size // self.chunk_size) + 1
		self.ac_num += chunk_num
		if chunk_num > 1:		# chunk 개수가 2개 이상일때는 청크 단위로 더 할당 받아야됨
			new_node = Node(self.chunk_size)
			self.node_list(size, new_node, chunk_num - 1)
		else:	# chunk 개수가 한개일 때
			new_node = Node(size)

		if self.arena[id] is None:		# 메모리 안의 청크가 비어있을 때, 할당 가능
			self.arena[id] = new_node
		else:							# 메모리 안의 청크가 이미 할당이 되어있는 경우, 비어있는 청크를 찾는다.
			curr = self.arena[id]
			while curr.next:
				curr = curr.next
			curr.next = new_node

		self.in_use_size += size

	def free(self, id):		# O(n)
		curr = self.arena[id]

		if curr is None:
			print("free: No such ID in hash table")
			return

		# in_use 사이즈 업데이트
		while curr:
			self.in_use_size -= curr.size
			curr = curr.next

        # 해당 ID의 청크 모두 삭제
		self.arena[id] = None

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