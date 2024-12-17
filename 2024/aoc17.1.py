import re
import sys

class Computer:
    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.instruction_pointer = 0
        self.output = ''

    def combo(self, operand):
        if operand >= 0 and operand <= 3:
            return operand
        if operand >= 4 and operand <= 6:
            return self.registers[chr(ord('A') + operand - 4)]
        raise Exception(f'Unexpected operand: {operand}')

    def execute(self):
        opcode, operand = self.program[self.instruction_pointer], self.program[self.instruction_pointer + 1]
        # print('>', self.instruction_pointer, opcode, operand)
        if opcode == 0:
            self.registers['A'] = self.registers['A'] // (2 ** self.combo(operand))
            self.instruction_pointer = self.instruction_pointer + 2
            return
        
        if opcode == 1:
            self.registers['B'] = self.registers['B'] ^ operand
            self.instruction_pointer = self.instruction_pointer + 2
            return
        
        if opcode == 2:
            self.registers['B'] = self.combo(operand) % 8
            self.instruction_pointer = self.instruction_pointer + 2
            return
        
        if opcode == 3:
            if self.registers['A'] == 0:
                self.instruction_pointer = self.instruction_pointer + 2
                return
            self.instruction_pointer = operand
            return
        
        if opcode == 4:
            self.registers['B'] = self.registers['B'] ^ self.registers['C']
            self.instruction_pointer = self.instruction_pointer + 2
            return
        
        if opcode == 5:
            self.output = self.output + str(self.combo(operand) % 8) + ','
            self.instruction_pointer = self.instruction_pointer + 2
            return

        if opcode == 6:
            self.registers['B'] = self.registers['A'] // (2 ** self.combo(operand))
            self.instruction_pointer = self.instruction_pointer + 2
            return

        if opcode == 7:
            self.registers['C'] = self.registers['A'] // (2 ** self.combo(operand))
            self.instruction_pointer = self.instruction_pointer + 2
            return

        raise Exception(f'Unexpected operation: {opcode}, {operand}')
    
    def can_execute(self):
        return self.instruction_pointer < len(self.program)

if __name__ == '__main__':
    
    registers = dict()
    for line in sys.stdin:
        if len(line.strip()) == 0:
            break
        register, value = re.findall('Register (.): (.+)', line.strip())[0]
        registers[register] = int(value)

    program = None
    for line in sys.stdin:
        program = list(map(int, line.strip().split(': ')[1].split(',')))
    
    print(program)
    computer = Computer(registers, program)
    while computer.can_execute():
        computer.execute()
    print(computer.output)