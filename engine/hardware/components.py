import numpy as np

from common.exceptions import NotAllowedError
from common.types import BitString, Register

_ram_capacity_in_word = 2**7  # * _word_in_byte/8 = 256B
_word_in_btye = 2


class Registers(object):

    # STATIC VARIABLES #
    _init_registers = [Register(i) for i in range(8)]
    _registers = {
        'r0':  _init_registers[0], 'zero': _init_registers[0],
        'r1':  _init_registers[1],  # 'at': _init_registers[1],
        'r2':  _init_registers[2],  # 'v0': _init_registers[2],
        'r3':  _init_registers[3],  # 'v1': _init_registers[3],
        'r4':  _init_registers[4],  # 'a0': _init_registers[4],
        'r5':  _init_registers[5], 'ra': _init_registers[5],
        'r6':  _init_registers[6], 'sp': _init_registers[6],
        'r7':  _init_registers[7], 'rd': _init_registers[7],
    }
    _registers['sp'].setRegisterValue(_ram_capacity_in_word * _word_in_btye)

    # DUNDERS #

    # PROPERTIES #

    # PUBLIC METHODS #
    @staticmethod
    def getRegister(register_id: str) -> Register:
        if isinstance(register_id, int):
            return Registers._init_registers[register_id]
        return Registers._registers[register_id]

    @staticmethod
    def resetRegisters():
        for register in Registers._init_registers:
            register.setRegisterValue(0)
        Registers._registers['sp'].setRegisterValue(
            _ram_capacity_in_word * _word_in_btye)

    # PRIVATE METHODS #


class Memory(object):

    # STATIC VARIABLES #
    _memory = np.zeros((_ram_capacity_in_word,), dtype=np.uint16)

    # DUNDERS #

    # PROPERTIES #

    # PUBLIC METHODS #
    @staticmethod
    def loadByte(address, offset=0) -> int:
        primary_index = ((address + offset) //
                         _word_in_btye) % _ram_capacity_in_word
        secondary_index = (address + offset) % _word_in_btye

        word = BitString(Memory._memory[primary_index])

        return word[secondary_index*8:secondary_index*8 + 8].value

    @staticmethod
    def storeByte(address, offset=0, value=0):
        primary_index = ((address + offset) //
                         _word_in_btye) % _ram_capacity_in_word
        secondary_index = (address + offset) % _word_in_btye

        word = BitString(Memory._memory[primary_index])
        adding_string = BitString(value, length=8)

        word[secondary_index*8:(secondary_index+1)*8] = adding_string
        Memory._memory[primary_index] = word.value

    @staticmethod
    def loadWord(address, offset=0) -> int:
        return (Memory.loadByte(address, offset) << 8) + \
            Memory.loadByte(address, offset+1)

    @staticmethod
    def storeWord(address, offset=0, value=0):
        adding_string = BitString(value, _word_in_btye * 8)
        Memory.storeByte(address, offset, adding_string[:8].value)
        Memory.storeByte(address, offset+1, adding_string[8:].value)

    @staticmethod
    def resetMemory():
        Memory._memory = np.zeros((_ram_capacity_in_word,), dtype=np.uint16)

    # PRIVATE METHODS #


class InstructionMemory(object):

    # STATIC VARIABLES #
    PC = 0
    _instructions: list = []

    # DUNDERS #

    # PROPERTIES #

    # PUBLIC METHODS #
    @staticmethod
    def load_instructions(instructions: list):
        InstructionMemory._instructions = instructions[:]
        InstructionMemory.PC = 0

    @staticmethod
    def next_instruction() -> list:
        InstructionMemory.PC += _word_in_btye
        try:
            return InstructionMemory._instructions[(
                InstructionMemory.PC-_word_in_btye)//_word_in_btye]
        except IndexError as e:
            return None

    # PRIVATE METHODS #
