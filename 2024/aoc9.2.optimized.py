import bisect
import sys
import time

# timothy@MacBook-Pro 2024 % python3 aoc9.2.py < inp9.2.txt
# --- defrag : 10.150997161865234 seconds ---
# --- checksum : 3.768112897872925 seconds ---
# 6286182965311
# timothy@MacBook-Pro 2024 % python3 aoc9.2.optimized.py < inp9.2.txt
# --- defrag : 0.015565156936645508 seconds ---
# --- checksum : 0.009240150451660156 seconds ---
# 6286182965311

def timer(name, func):
    start_time = time.time()
    ret_val = func()
    print(f"--- {name} : {time.time() - start_time} seconds ---")
    return ret_val

class Block:
    def __init__(self, size, file_id, moved=False):
        self.size = size
        self.file_id = file_id
        self.moved = moved
        self.next = None
        self.prev = None
        self.id = None

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f'({self.id}, {self.size}, {self.file_id})'
    
    def is_free(self):
        return self.file_id is None

class Memory:
    def __init__(self, blocks):
        self.head, self.tail = self.connect_blocks(blocks)
        self.free_blocks_index = self.index_free_blocks()
    
    def connect_blocks(self, blocks):
        prev = None
        next = None
        for i in range(len(blocks)):
            blocks[i].id = i
            blocks[i].prev = prev
            prev = blocks[i]
            blocks[len(blocks) - i - 1].next = next
            next = blocks[len(blocks) - i - 1]
        return blocks[0], blocks[-1]
    
    def index_free_blocks(self):
        index = {}
        head = self.head
        while head is not None:
            if head.is_free():
                free_list = index.get(head.size, list())
                free_list.append(head)
                index[head.size] = free_list
            head = head.next
        return index
    
    def get_leftmost_free_block(self, defrag_block):
        free_sizes = [free_size for free_size in self.free_blocks_index if free_size >= defrag_block.size]
        leftmost_free_block = None
        for free_size in free_sizes:
            free_blocks = self.free_blocks_index.get(free_size, list())
            if len(free_blocks) == 0:
                continue
            if free_blocks[0].id > defrag_block.id:
                continue
            if leftmost_free_block is None:
                leftmost_free_block = free_blocks[0]
            if leftmost_free_block.id > free_blocks[0].id:
                leftmost_free_block = free_blocks[0]
        return leftmost_free_block
    
    def remove_free_block_from_index(self, free_block):
        self.free_blocks_index[free_block.size].remove(free_block)

    def add_free_block_to_index(self, free_block):
        free_list = self.free_blocks_index.get(free_block.size, list())
        bisect.insort(free_list, free_block, key=lambda block: block.id)
        self.free_blocks_index[free_block.size] = free_list

    def defrag(self):
        tail = self.tail
        while True:
            if tail is None:
                break

            if tail.is_free() or tail.size == 0 or tail.moved:
                tail = tail.prev
                continue
            defrag_block = tail
            
            head = self.get_leftmost_free_block(defrag_block)
            if head is None:
                tail = tail.prev
                continue
            free_block = head

            frag_block = Block(defrag_block.size, defrag_block.file_id, True)
            free_block.prev.next = frag_block
            frag_block.prev = free_block.prev

            if free_block.size > defrag_block.size:
                self.remove_free_block_from_index(free_block)
                free_block.size = free_block.size - defrag_block.size
                frag_block.next = free_block
                free_block.prev = frag_block
                frag_block.id = (frag_block.prev.id + frag_block.next.id) / 2
                self.add_free_block_to_index(free_block)
            elif free_block.size == defrag_block.size:
                self.remove_free_block_from_index(free_block)
                free_block.next.prev = frag_block
                frag_block.next = free_block.next
                frag_block.id = free_block.id
            else:
                raise Exception('Unexpected')

            defrag_block.file_id = None
    
    def get_layout(self):        
        mem_str = []
        head = self.head
        while head is not None:
            if head.is_free():
                mem_str.extend(['.'] * head.size)
            else:
                mem_str.extend([head.file_id] * head.size)
            head = head.next
        return mem_str
    
    def checksum(self):
        checksum = 0
        layout = self.get_layout()
        for i in range(len(layout)):
            if layout[i] == '.':
                continue
            checksum = checksum + i * int(layout[i])
        return checksum

    def print_layout(self):
        print(self.get_layout())

    def get_blocks(self):
        blocks = []
        head = self.head
        while head is not None:
            blocks.append(head)
            head = head.next
        return blocks

    def print(self):
        print(self.get_blocks())

if __name__ == '__main__':
    inp = sys.stdin.readline().strip()
    # print(inp)
    
    mem = Memory([Block(int(inp[i]), str(i//2) if i % 2 == 0 else None) for i in range(len(inp))])
    timer('defrag', mem.defrag)
    # mem.print_layout()
    print(timer('checksum', mem.checksum))
