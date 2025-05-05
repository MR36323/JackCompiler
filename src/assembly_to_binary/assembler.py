class Assembler:

    def __init__(self, asm_lines):
        self.asm_lines = asm_lines
        self.word_length = 16
        self.__buffer = ""

    def __iter__(self):
        return self

    def __next__(self):
        asm_instruction = next(self.asm_lines)
        bin_instruction = self.__translate_asm(asm_instruction)
        self.__add_to_buffer(bin_instruction)
        return self.__empty_buffer()       
    
    def __translate_asm(self, asm_instruction):
        if asm_instruction.startswith("@"):                         
            return self.__translate_A_instruction(asm_instruction)
    
    def __translate_A_instruction(self, A_instruction):                                                 
        asm_instruction = int(A_instruction.lstrip("@"))
        bin_instruction = str(bin((int(asm_instruction)) % 2**15))[2:]  # Max integer size is 2^15 - 1
        while len(bin_instruction) < self.word_length:         
            bin_instruction = "".join(("0", bin_instruction))      
        return bin_instruction

    def __add_to_buffer(self, bin_instruction):
        if not self.__buffer:
            self.__buffer = bin_instruction
        else:
            self.__buffer.append(f"\n{bin_instruction}")

    def __empty_buffer(self):
        buffer = self.__buffer
        self.__buffer = ""
        return buffer