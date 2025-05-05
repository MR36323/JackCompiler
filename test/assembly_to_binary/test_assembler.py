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
    
    def test_a_instructions_within_range(self):    # Max integer size is 2^15 - 1
        input = ["@0", "@1", "@32767"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assembler = Assembler(iter(input))
        assert expected == list(assembler)

    def test_a_instructions_outside_range(self):    # Max integer size is 2^15 - 1
        input = ["@32768", "@32769", "@65535"]
        expected = ["0000000000000000", "0000000000000001", "0111111111111111"]
        assembler = Assembler(iter(input))
        assert expected == list(assembler)
