from engine.hardware.components import InstructionMemory
from engine.software.instructionFunctions import instruction_functions


class Processor(object):

    # PUBLIC METHODS #
    @staticmethod
    def processNext():
        current_instruction = InstructionMemory.next_instruction()
        if current_instruction is None:
            return None

        raw_changed_regs, changed_mems = instruction_functions[
            current_instruction[0]](*current_instruction[1:])

        changed_regs = []
        for reg_id, old_reg in raw_changed_regs:
            changed_regs.append((reg_id, old_reg))

        return changed_regs, changed_mems
