import time
import sys

def timer(name, func):
    start_time = time.time()
    ret_val = func()
    print(f"--- {name} : {time.time() - start_time} seconds ---")
    return ret_val

class Block:
    def __init__(self, size, file_id):
        self.size = size
        self.file_id = file_id

    def __repr__(self):
        return f'({self.size}, {self.file_id})'
    
    def is_free(self):
        return self.file_id is None

class Memory:
    def __init__(self, blocks):
        self.blocks = blocks

    def defrag(self):
        start_idx = 0
        end_idx = len(self.blocks) - 1
        while True:
            # print(start_idx, end_idx)
            # print(self.blocks)
            if start_idx == end_idx:
                break
            free_block = self.blocks[start_idx]
            if not free_block.is_free() or free_block.size == 0:
                start_idx = start_idx + 1
                continue
            
            defrag_block = self.blocks[end_idx]
            if defrag_block.is_free() or defrag_block.size == 0:
                end_idx = end_idx - 1
                continue
            
            frag_block = Block(min(defrag_block.size, free_block.size), defrag_block.file_id)

            new_blocks = self.blocks[:start_idx] + [frag_block] 
            end_idx = end_idx + 1
            
            if free_block.size > defrag_block.size:
                remaining_free_block = Block(free_block.size - defrag_block.size, None)
                new_blocks = new_blocks + [remaining_free_block]
                defrag_block.file_id = None
            elif free_block.size < defrag_block.size:
                defrag_block.size = defrag_block.size - free_block.size
            else:
                defrag_block.size = 0
                defrag_block.file_id = None

            self.blocks = new_blocks + self.blocks[start_idx + 1:]
    
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

