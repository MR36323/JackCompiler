class Assembler:

    def __init__(self, asm_lines):
        self.asm_lines = asm_lines
        self.word_length = 16
        self.__buffer = ""

    def __iter__(self):
        return self

    def __next__(self):
        asm_instruction = next(self.asm_lines)
        bin_instruction = self.__parse_and_translate(asm_instruction)
        self.__add_to_buffer(bin_instruction)
        return self.__empty_buffer()       
    
    def __parse_and_translate(self, asm_instruction):
        if asm_instruction.startswith("@"):                                    # A-instructions start with @
            return self.__translate_A_instruction(asm_instruction)
        split_on_dest_seperator = asm_instruction.split("=")
        try:
            dest = split_on_dest_seperator[0]
            asm_minus_dest = split_on_dest_seperator[1]
        except IndexError:
            dest = None
            asm_minus_dest = split_on_dest_seperator[0]
        split_on_jump_seperator = asm_minus_dest.split(";")    
        try:
            comp = split_on_jump_seperator[0]
            jump = split_on_jump_seperator[1]
        except IndexError:
            comp = split_on_jump_seperator[0]
            jump = None
        return self.__translate_C_instruction(dest, comp, jump)
    
    def __translate_A_instruction(self, A_instruction):                                                 
        asm_instruction = int(A_instruction.lstrip("@"))
        bin_instruction = str(bin((int(asm_instruction)) % 2**15))[2:]         # Max integer size is 2^15 - 1
        while len(bin_instruction) < self.word_length:         
            bin_instruction = "".join(("0", bin_instruction))      
        return bin_instruction
    
    def __translate_C_instruction(self, asm_dest, asm_comp, asm_jump):
        comps = { 
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }
        dests = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }
        jumps = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
        bin_C_instruction = comps[asm_comp]
        if asm_dest:
            bin_C_instruction = "".join((bin_C_instruction, dests[asm_dest]))
        else:
            bin_C_instruction = "".join((bin_C_instruction, "000"))
        if asm_jump:
            bin_C_instruction = "".join((bin_C_instruction, jumps[asm_jump]))
        else:
            bin_C_instruction = "".join((bin_C_instruction, "000"))
        return "".join(("111", bin_C_instruction))

    def __add_to_buffer(self, bin_instruction):
        if not self.__buffer:
            self.__buffer = bin_instruction
        else:
            self.__buffer.append(f"\n{bin_instruction}")

    def __empty_buffer(self):
        if not self.__buffer:
            return None
        buffer = self.__buffer
        self.__buffer = ""
        return buffer