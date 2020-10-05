"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xf4
        self.pc = 0
        self.fl = 0b00000000
        self.running = False
        # self.branchtable = {
        #     0b10000010: self.LDI(),
        #     0b01000111: self.PRN(),

        # }


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        program = sys.argv[1]

        with open(program) as p:
            for instruction in p:
                if instruction[0] == '#':
                    continue

                instruction = instruction.strip()
                temp = instruction.split()

                if len(temp) == 0:
                    continue

                self.ram[address] = int(temp[0], 2)
                address += 1
    
        # print("======= PROGRAM =========")
        # for i in self.ram[:35]:
        #     print(i)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = self.fl | 0b00000001
            else:
                self.fl = self.fl & 0b11111110

            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = self.fl | 0b00000010
            else:
                self.fl = self.fl & 0b11111101

            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = self.fl | 0b00000100
            else:
                self.fl = self.fl & 0b11111011
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # def LDI(self):
    #     self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
    #     self.pc += 3

    # def PRN(self):
    #     print(self.reg[self.ram[self.pc+1]])
    #     self.pc += 2


    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        JMP = 0b01010100
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        
        self.running = True
       
        while self.running == True: 
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI: 
                self.reg[operand_a] = operand_b
                self.pc += 3
            

            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += 2


            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3


            elif instruction == HLT:
                self.running = False


            elif instruction == PUSH:
                self.reg[7] -= 1

                stack_top = self.reg[7]
                self.ram[stack_top] = self.reg[operand_a]

                self.pc += 2


            elif instruction == POP:
                stack_top = self.reg[7]
                self.reg[operand_a] = self.ram[stack_top]

                self.reg[7] += 1
                
                self.pc += 2


            elif instruction == CALL:
                self.reg[7] -=1

                stack_top = self.reg[7]
                self.ram[stack_top] = self.pc + 2

                self.pc = self.reg[operand_a]
                # print(f"PC = {self.pc}")
                # print(f"CALL INVOKED. REGISTER 7 set to {self.reg[7]}")


            elif instruction == RET:
                stack_top = self.reg[7]
                self.pc = self.ram[stack_top]

                self.reg[7] +=1
                # print(f"RETURN INVOKED. REGISTER 7 set to {self.reg[7]}")

            
            elif instruction == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            
            elif instruction == JMP:
                self.pc = self.reg[operand_a]


            elif instruction == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3


            elif instruction == JEQ:
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            
            elif instruction == JNE:
                check_e = self.fl & 0b00000001
                if check_e == 0b00000000:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
                
