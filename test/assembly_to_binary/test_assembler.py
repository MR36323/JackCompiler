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
        assembler = Assembler(iter(input))
        assert expected == list(assembler)


class TestAssemblyWithoutSymbols:
    
    def test_a_instructions_within_range(self):    
        input = ["@0", "@1", "@32767"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assembler = Assembler(iter(input))
        assert expected == list(assembler)

    def test_a_instructions_outside_range(self):    # Max integer size is 2^15 - 1
        input = ["@32768", "@32769", "@65535"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assembler = Assembler(iter(input))
        assert expected == list(assembler)

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

        assembler = Assembler(iter(asm_c_instructions))
        assert bin_c_instructions == list(assembler)