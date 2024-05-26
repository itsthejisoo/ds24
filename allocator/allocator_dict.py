class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena = dict()
        self.in_use_size = 0	# 사용 중인 메모리 크기
        self.ac_num = 0	        # arena 안에 있는 청크 총 개수
        
    def print_stats(self):
        arena_size = self.ac_num * self.chunk_size
        utilization = self.in_use_size / arena_size if arena_size > 0 else 0

		# MB단위이므로 1M 나누기
        print("Arena: ", arena_size // (1024 * 1024), "MB")
        print("In-use: ", self.in_use_size // (1024 * 1024), "MB")
        print("Utilization: {:.3f}".format(utilization))

    def malloc(self, id, size):                     # 할당해야할 청크 개수 구하고 딕셔너리에 추가하기
        chunk_num = (size // self.chunk_size) + 1
        self.ac_num += chunk_num
        if chunk_num == 1:
            self.arena[id] = [size]
        if chunk_num > 1:                          # chunk 개수가 2개 이상일 경우 dictionary에 chunk 리스트를 저장한다.
            if id in self.arena:                    # arena에 이미 id가 존재하고 추가로 chunk 할당할 경우
                self.arena.append(size - (self.chunk_size * (chunk_num - 1)))
            else:
                chunk_arr = [self.chunk_size] * (chunk_num - 1)
                chunk_arr.append(size - (self.chunk_size * (chunk_num - 1)))
                self.arena[id] = chunk_arr
        self.in_use_size += size
    
    def free(self, id):
        if id not in self.arena:
            print("free: No such ID in hash table")
            return

        if isinstance(self.arena[id], list):        # self.arena[id]의 type가 list인지 확인하는 조건문 -> true: chunk가 2개 이상
            free_size = ((len(self.arena[id]) - 1) * 4096) + self.arena[id][len(self.arena[id]) - 1]
            self.in_use_size -= free_size
        else:                                       # chunk가 1개일 경우
            self.in_use_size -= self.arena[id][0]

        del self.arena[id]


if __name__ == "__main__":
    allocator = Allocator()
    
    with open ("allocator/input.txt", "r") as file:
        n=0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            # if n%100 == 0:
            #     print(n, "...")
            
            n+=1
    
    allocator.print_stats()