import sys
import time
import uuid

# timothy@MacBook-Pro 2024 % python3 aoc9.1.py < inp9.2.txt 
# --- defrag : 1.2495479583740234 seconds ---
# --- checksum : 3.9852001667022705 seconds ---
# 6258319840548
# timothy@MacBook-Pro 2024 % python3 aoc9.1.optimized.py < inp9.2.txt
# --- defrag : 0.02288508415222168 seconds ---
# --- checksum : 0.008285760879516602 seconds ---
# 6258319840548

def timer(name, func):
    start_time = time.time()
    ret_val = func()
    print(f"--- {name} : {time.time() - start_time} seconds ---")
    return ret_val

class Block:
    def __init__(self, size, file_id):
        self.size = size
        self.file_id = file_id
        self.next = None
        self.prev = None
        self.uuid = uuid.uuid4()
    
    def __eq__(self, other):
        return self.uuid == other.uuid

    def __repr__(self):
        return f'({self.size}, {self.file_id})'
    
    def is_free(self):
        return self.file_id is None

class Memory:
    def __init__(self, blocks):
        self.head, self.tail = self.connect_blocks(blocks)
    
    def connect_blocks(self, blocks):
        prev = None
        next = None
        for i in range(len(blocks)):
            blocks[i].prev = prev
            prev = blocks[i]
            blocks[len(blocks) - i - 1].next = next
            next = blocks[len(blocks) - i - 1]
        return blocks[0], blocks[-1]

    def defrag(self):
        head = self.head
        tail = self.tail
        while True:
            # print("====")
            # print(head, tail)
            # self.print()
            # self.print_layout()
            if head is None or tail is None or head == tail:
                break
            
            if not head.is_free() or head.size == 0:
                head = head.next
                continue
            free_block = head
            
            if tail.is_free() or tail.size == 0:
                tail = tail.prev
                continue
            defrag_block = tail
            
            frag_block = Block(min(defrag_block.size, free_block.size), defrag_block.file_id)
            free_block.prev.next = frag_block
            frag_block.prev = free_block.prev
            head = frag_block

            if free_block.size > defrag_block.size:
                free_block.size = free_block.size - defrag_block.size
                frag_block.next = free_block
                free_block.prev = frag_block
                defrag_block.file_id = None
            elif free_block.size <= defrag_block.size:
                defrag_block.size = defrag_block.size - free_block.size
                frag_block.next = free_block.next
                free_block.next.prev = frag_block
                defrag_block.file_id = None if defrag_block.size == 0 else defrag_block.file_id
    
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
    print(timer('checksum', mem.checksum))

