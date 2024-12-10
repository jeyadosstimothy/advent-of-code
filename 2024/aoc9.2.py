import sys
import time

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

    def __repr__(self):
        return f'({self.size}, {self.file_id})'
    
    def is_free(self):
        return self.file_id is None

class Memory:
    def __init__(self, blocks):
        self.blocks = blocks

    def defrag(self):
        end_idx = len(self.blocks) - 1
        while True:
            if end_idx == 0:
                break

            defrag_block = self.blocks[end_idx]
            if defrag_block.is_free() or defrag_block.size == 0 or defrag_block.moved:
                end_idx = end_idx - 1
                continue
            
            free_idx = 0
            free_block = self.blocks[free_idx]
            while free_idx < len(self.blocks) and (not free_block.is_free() or free_block.size == 0 or free_block.size < defrag_block.size):
                free_idx = free_idx + 1
                if free_idx == len(self.blocks):
                    break
                free_block = self.blocks[free_idx]
                continue
            
            if free_idx == len(self.blocks) or free_idx > end_idx:
                end_idx = end_idx - 1
                continue

            # print(free_idx, end_idx, self.blocks)
            
            moved_block = Block(defrag_block.size, defrag_block.file_id, True)

            new_blocks = self.blocks[:free_idx] + [moved_block] 
            end_idx = end_idx + 1
            
            if free_block.size > defrag_block.size:
                remaining_free_block = Block(free_block.size - defrag_block.size, None)
                new_blocks = new_blocks + [remaining_free_block]
            
            defrag_block.file_id = None

            self.blocks = new_blocks + self.blocks[free_idx + 1:]
    
    def get_layout(self):
        mem_str = []
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if block.is_free():
                mem_str = mem_str + ['.'] * block.size
            else:
                mem_str = mem_str + [block.file_id] * block.size
        return mem_str

    def checksum(self):
        checksum = 0
        layout = self.get_layout()
        for i in range(len(layout)):
            if layout[i] == '.':
                continue
            checksum = checksum + i * int(layout[i])
        return checksum

    def __repr__(self):
        return str(self.get_layout())

if __name__ == '__main__':
    inp = sys.stdin.readline().strip()
    # print(inp)
    
    mem = Memory([Block(int(inp[i]), str(i//2) if i % 2 == 0 else None) for i in range(len(inp))])
    # print(mem)
    timer('defrag', mem.defrag)
    # print(mem)
    print(timer('checksum', mem.checksum))


