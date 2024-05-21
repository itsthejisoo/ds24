class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena_size = 0
        self.in_use = 0
        self.free_space = 0
        self.hash_table = ChainedHashTable(100000)

    def print_stats(self):
        print(f"Arena: {self.arena_size / (1024 * 1024):.2f} MB")
        print(f"In-use: {self.in_use / (1024 * 1024):.2f} MB")
        utilization = self.in_use / self.arena_size if self.arena_size != 0 else 0
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        if size % self.chunk_size != 0:
            size = (size // self.chunk_size + 1) * self.chunk_size
        if size > self.free_space:
            additional_chunks = (size - self.free_space + self.chunk_size - 1) // self.chunk_size
            self.arena_size += additional_chunks * self.chunk_size
            self.free_space += additional_chunks * self.chunk_size
        self.hash_table.insert(id, size)
        self.in_use += size
        self.free_space -= size
        print(f"Allocated memory {id} of size {size} bytes")

    def free(self, id):
        size = self.hash_table.delete(id)
        if size:
            self.in_use -= size
            self.free_space += size
            print(f"Freed memory {id} of size {size} bytes")
        else:
            print(f"Error: Memory {id} not found")


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