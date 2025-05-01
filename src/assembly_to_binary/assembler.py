class Assembler:

    def __init__(self, assembly_lines):
        self.assembly_lines = assembly_lines

    def __iter__(self):
        return self

    def __next__(self):
        asm_instruction = next(self.assembly_lines)

        if asm_instruction.startswith("@"):                         # If A-instruction
            asm_instruction = int(asm_instruction.lstrip("@"))
            bin_instruction = str(bin(asm_instruction)[2:])
            while len(bin_instruction) < 16:                        # All A-instructions start with 0 and are 16-bits long               
                bin_instruction = "".join(("0", bin_instruction))      
        
        return bin_instruction 
        