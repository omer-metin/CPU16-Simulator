from common.definitions import *
from common.types import *
from engine.hardware.components import Registers


class MIPSAssembler(object):

    # STATIC VARIABLES #
    _current_instructions = None

    # DUNDERS #

    # PROPERTIES #

    # PUBLIC METHODS #
    @staticmethod
    def assembly(source: str, toMachineCode=False) -> list:
        MIPSAssembler._current_instructions = MIPSAssembler._tokenizer(
            source)

        MIPSAssembler._setRegister()
        MIPSAssembler._setImmediates()
        MIPSAssembler._setMemoryLocations()
        MIPSAssembler._setControlBits()

        # FIXME: return before setting opcodes for this state of project
        if not toMachineCode:
            return MIPSAssembler._current_instructions[:]

        instructions = MIPSAssembler._setOpcodes()
        machine_codes = []
        for instruction in instructions:
            machine_codes.append(instruction.toMachineCode())

        return machine_codes

    # PRIVATE METHODS #
    @staticmethod
    def _tokenizer(source) -> list:
        lines = []
        for raw_line in source.splitlines():
            if len(raw_line.strip()) > 0:
                line = raw_line.split('#')[0].replace('\t', ' ')
                if line.find(':') >= 0:
                    splitted_line = line.split(':')
                    for block_line in splitted_line[:-1]:
                        if len(block_line.strip()) > 0:
                            lines.append(block_line + ':')
                    if len(splitted_line[-1].strip()) > 0:
                        lines.append(splitted_line[-1])
                    continue
                lines.append(line)

        blocks = {}
        for idx, line in enumerate(lines):
            if line.find(':') >= 0:
                blocks[line[:-1]] = idx - len(blocks)

        words = []
        for idx, line in enumerate(lines):
            if line.find(':') >= 0:
                continue

            line_words = []
            splitted_line = line.split()
            for idx2, raw_word in enumerate(splitted_line):
                if len(raw_word) > 0:
                    if raw_word in blocks:
                        if splitted_line[idx2 - 1].startswith('j'):
                            line_words.append(
                                str((blocks[raw_word])*2))
                        else:
                            line_words.append(str((
                                blocks[raw_word] - idx - 1)*2))
                    else:
                        line_words.append(raw_word)

            if len(line_words) > 0:
                words.append(line_words)
        return words

    @staticmethod
    def _setOpcodes() -> list:
        instructions = []
        for instruction in MIPSAssembler._current_instructions:
            instruction_key = instruction[0]
            opcode = opcodes[instruction_key]
            instruction[0] = opcode
            inst_dict: dict = instruction_machinecode_orders[instruction_key]
            if opcode == 0b1000:
                inst_dict.update(dict(
                    zip(instruction_assembly_orders[instruction_key],
                        instruction)))
                instructions.append(R_Type(**inst_dict))
            else:
                inst_dict.update(dict(
                    zip(instruction_assembly_orders[instruction_key],
                        instruction)))
                instructions.append(I_Type(**inst_dict))

        return instructions

    @staticmethod
    def _setRegister():
        for instruction in MIPSAssembler._current_instructions:
            for i, word in enumerate(instruction):
                if isinstance(word, str) and word.startswith('$'):
                    try:
                        instruction[i] = Registers.getRegister(
                            word.strip('$,'))
                    except Exception as e:
                        raise e

    @staticmethod
    def _setImmediates():
        for instruction in MIPSAssembler._current_instructions:
            for i, word in enumerate(instruction):
                if isinstance(word, str):
                    try:
                        instruction[i] = int(word)
                    except ValueError as e:
                        pass

    @staticmethod
    def _setMemoryLocations():
        for instruction in MIPSAssembler._current_instructions:
            for i, word in enumerate(instruction):
                if isinstance(word, str) and word.find('(') >= 0:
                    offset_part, address_part = word.split('(', 1)
                    address = address_part.strip(')')
                    instruction[i] = Registers.getRegister(
                        address.strip('$,)'))
                    instruction.append(int(offset_part))

    @staticmethod
    def _setControlBits():
        for instruction in MIPSAssembler._current_instructions:
            for i, word in enumerate(instruction):
                if isinstance(word, str) and word.endswith('c'):
                    instruction[i] = word[:-1]
                    instruction.insert(i+1, 0)
                elif (isinstance(instruction[i], str) and
                      ctrl in instruction_assembly_orders[instruction[i]]):
                    instruction.insert(i+1, 1)
