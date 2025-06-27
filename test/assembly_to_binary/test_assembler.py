import pytest
from src.assembly_to_binary.assembler import Assembler

class TestIteratorBehaviour:

    def test_next_method(self):
        input = ["@0", "@1", "@2"]
        expected = ["0000000000000000", "0000000000000001", "0000000000000010"]
        assembler = Assembler(iter(input))
        output = [next(assembler) for _ in range(len(input))]
        assert output == expected

    def test_raises_stop_iteration(self):
        input = ["@0", "@1", "@2"]
        assembler = Assembler(iter(input))
        for _ in range(len(input)):
            next(assembler)
        with pytest.raises(StopIteration):
            next(assembler)

    def test_list_conversion(self):
        input = ["@0", "@1", "@2"]
        expected = ["0000000000000000", "0000000000000001", "0000000000000010"]
        assert expected == list(Assembler(iter(input)))

class TestAssemblyWithoutSymbols:
    
    def test_a_instructions_within_range(self):    
        input = ["@0", "@1", "@32767"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assert expected == list(Assembler(iter(input)))

    def test_a_instructions_outside_range(self):    # Max integer size is 2^15 - 1
        input = ["@32768", "@32769", "@65535"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assert expected == list(Assembler(iter(input)))

    def test_c_instructions(self):
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

        asm_c_instructions = []                                     # All C-instructions in assembly
        dests_comps = []
        for comp in comps:                                          # C-instruction syntax: dest=comp;jump
            for dest in dests:
                if dest!= "null":
                    dests_comps.append("=".join((dest, comp)))
                else:
                    dests_comps.append(comp)                    
        for dest_comp in dests_comps:
            for jump in jumps:
                if jump!= "null":
                    asm_c_instructions.append(";".join((dest_comp, jump)))
                else:
                    asm_c_instructions.append(dest_comp)   

        bin_c_instructions = []                                    # All C-instructions in binary
        dests_comps = []
        for comp in comps.values():                                          
            for dest in dests.values():
                dests_comps.append(comp.join(("111", dest)))                       
        for dest_comp in dests_comps:
            for jump in jumps.values():
                bin_c_instructions.append("".join((dest_comp, jump)))

        assert bin_c_instructions == list(Assembler(iter(asm_c_instructions)))

class TestAssemblyWithSymbols:

    def test_pre_defined_symbols(self):
        a_instructions = [
            '@R0', 
            '@R1', 
            '@R2', 
            '@R3', 
            '@R4', 
            '@R5', 
            '@R6', 
            '@R7', 
            '@R8', 
            '@R9', 
            '@R10', 
            '@R11', 
            '@R12', 
            '@R13', 
            '@R14', 
            '@R15', 
            '@SCREEN', 
            '@KBD', 
            '@SP', 
            '@LCL', 
            '@ARG', 
            '@THIS', 
            '@THAT'
        ]
        expected_output = [
            '0000000000000000', 
            '0000000000000001', 
            '0000000000000010', 
            '0000000000000011', 
            '0000000000000100', 
            '0000000000000101', 
            '0000000000000110', 
            '0000000000000111', 
            '0000000000001000', 
            '0000000000001001', 
            '0000000000001010', 
            '0000000000001011', 
            '0000000000001100', 
            '0000000000001101', 
            '0000000000001110', 
            '0000000000001111', 
            '0100000000000000', 
            '0110000000000000', 
            '0000000000000000', 
            '0000000000000001', 
            '0000000000000010', 
            '0000000000000011', 
            '0000000000000100'
        ]
        assert expected_output == list(Assembler(iter(a_instructions)))

    def test_custom_variable_symbols(self):
        a_instructions = [
            '@i',
            '@i',
            '@x',
            '@y',
            '@i'
        ]
        expected_output = [
            '0000010000000000',          # new variables start at ram[1024]
            '0000010000000000',
            '0000010000000001',
            '0000010000000010',
            '0000010000000000',
        ]
        assert expected_output == list(Assembler(iter(a_instructions)))
