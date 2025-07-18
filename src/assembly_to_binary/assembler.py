class Assembler:

    def __init__(self, asm_lines):
        self.__word_length = 16
        self.__asm_lines = asm_lines
        self.__translated = []
        self.__assembled = []
        self.__variables  = {
            '@R0': 0,
            '@R1': 1,
            '@R2': 2,
            '@R3': 3,
            '@R4': 4,
            '@R5': 5,
            '@R6': 6,
            '@R7': 7,
            '@R8': 8,
            '@R9': 9,
            '@R10': 10,
            '@R11': 11,
            '@R12': 12,
            '@R13': 13,
            '@R14': 14,
            '@R15': 15,
            '@SCREEN': 16384,
            '@KBD': 24576,
            '@SP': 0,
            '@LCL': 1,
            '@ARG': 2,
            '@THIS': 3,
            '@THAT': 4,
        }
        self.__latest_var_value = 1023
        self.__labels = {}

    def assemble(self):
        while self.__asm_lines:
            asm_instruction = self.__asm_lines.pop(0)
            asm_instruction = self.__process_comment(asm_instruction)
            if asm_instruction:
                bin_instruction = self.__parse_and_translate(asm_instruction)
                if bin_instruction:
                    self.__translated.append(asm_instruction)
                    self.__assembled.append(bin_instruction)
        return self.__assembled
    
    def __parse_and_translate(self, asm_instruction):
        if asm_instruction.startswith('(') and asm_instruction.endswith(')'):
            return self.__translate_label(asm_instruction)                  # Label syntax: (label)
        if asm_instruction.startswith('@'):                                 # A-instructions start with @
            return self.__translate_A_instruction(asm_instruction)
        if '=' not in asm_instruction:                                      # C-instruction syntax: dest=comp;jump
            dest, asm_minus_dest = None, asm_instruction
        else:                                                          
            dest, asm_minus_dest = asm_instruction.split('=')            
        if ';' not in asm_instruction:
            jump, comp = None, asm_minus_dest
        else:
            comp, jump = asm_minus_dest.split(';')    
        return self.__translate_C_instruction(dest, comp, jump) 
    
    def __process_comment(self, asm_instruction):
        return asm_instruction.split('//')[0].strip()
    
    def __translate_label(self, label):
        label = label.lstrip('(').rstrip(')')
        if label not in self.__labels:
            self.__labels[label] = len(self.__assembled)
            if f'@{label}' in self.__translated:
                label_call = f'@{self.__labels[label]}'
                label_call = self.__translate_A_instruction(label_call)
                self.__assembled[self.__translated.index(f'@{label}')] = label_call
        
    def __translate_A_instruction(self, A_instruction):                                                 
        if A_instruction[1:].isnumeric():
            A_instruction = int(A_instruction.lstrip('@'))
        elif A_instruction.lstrip('@') in self.__labels:
            A_instruction = self.__labels[A_instruction.lstrip('@')]
        elif A_instruction in self.__variables:
            A_instruction = self.__variables[A_instruction]
        else:
            self.__latest_var_value += 1 
            self.__variables[A_instruction] = self.__latest_var_value
            A_instruction = self.__latest_var_value
        bin_instruction = str(bin((int(A_instruction)) % 2**15))[2:]      # Max integer size is 2^15 - 1
        while len(bin_instruction) < self.__word_length:         
            bin_instruction = ''.join(('0', bin_instruction))      
        return bin_instruction
    
    def __translate_C_instruction(self, asm_dest, asm_comp, asm_jump):
        comps = { 
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            'M': '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101'
        }
        dests = {
            'null': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111'
        }
        jumps = {
            'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }
        bin_C_instruction = comps[asm_comp]
        if asm_dest:
            bin_C_instruction = ''.join((bin_C_instruction, dests[asm_dest]))
        else:
            bin_C_instruction = ''.join((bin_C_instruction, '000'))
        if asm_jump:
            bin_C_instruction = ''.join((bin_C_instruction, jumps[asm_jump]))
        else:
            bin_C_instruction = ''.join((bin_C_instruction, '000'))
        return ''.join(('111', bin_C_instruction))