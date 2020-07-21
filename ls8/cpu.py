import sys

# commands
HLT   =  0x01    # op-code x01

LDI    =  0x82  # Set the value of a register to an integer.

                # Three bytes
                    # byte 0 - instruction
                    # byte 1 - register
                    # byte 2 - "immediate" a number 0 - 255


PRN    =  0x47  # Prints a value.
                # Two bytes
                    # byte 0 - instruction
                    # byte 1 - value to print


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0x00]*256
        
        # 8 general-purpose 8-bit numeric registers R0-R7.
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)
        self.registers = [0] * 8


        # Internal registers
        self.PC = 0  # Program Counter, address of currently executing instruction
        self.IR = 0  # Instruction Register, copy of currently executing instruction
        self.MAR = 0 # Memory Address Register, address we're reading or writing
        self.MDR = 0 # Memory Data Register, value to write or value just read
        self.FL = 0  # Flags
    
        # Flags
        # L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        # G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        # E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.



    def ram_read(self, MAR):
        """Accept the address to read and return the value stored there.
         MAR contains the address that is being read or written to.
        """
        return self.ram[MAR]


    def ram_write(self, MDR, val_to_write):
        """Should accept a value to write, and the address to write it to.
        MDR contains the data that was read or the data to write"""
        self.ram[MDR] = val_to_write
        return True

    


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
    
        while running:
            self.trace()
            command = self.ram[self.PC]
            # print(f'Command is x{command:X}')
            if command == HLT:
                # print(f'Command is HLT')
                # input()
                sys.exit("Hit an HLT command")
            elif command == LDI:
                # print(f'Command is LDI')
                reg = self.ram[self.PC+1]
                # print(f'Register to use is {reg}')
                self.registers[reg] = self.ram[self.PC+2] 
                # print(f'Value to place is {self.ram[self.PC+2]}')  
                # print(f'Register after placement is  {self.ram[self.PC+2]}')  
                self.PC += 1
                # print(f'self.pc is now {self.PC}')  
            elif command == PRN:
                # print(f'Command is PRN')
                # print(self.ram[self.PC+1])
                # print(f'Number to print is {self.ram[self.PC+1]}')
                self.PC += 1
                # print(f'self.pc is now {self.PC}')  
            self.PC += 1
            # print(f'self.pc is now {self.PC}')
            # input()

spanky = CPU()
spanky.load()
spanky.run()
