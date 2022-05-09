import numpy as np
from common.exceptions import *
from common.definitions import *


class BitString(object):

    # STATIC VARIABLES #

    # DUNDERS #
    def __init__(self, value=0, length=16):
        super().__init__()
        raw_value = value
        self._sign = 1
        self._length = length
        if not value:
            self._sign = 0
            self._string: np.ndarray = np.zeros((length,), dtype=np.uint8)
        else:
            value = raw_value % 2**self._length
            if raw_value < 0:
                value = raw_value % (2**self._length - 1)
                self._sign = -1
                value += 1
            bin_str = bin(value)[2:]
            self._string: np.ndarray = np.array(
                list('0'*(length-len(bin_str)) + bin_str), dtype=np.uint8)

    def __str__(self):
        return str(self._string).strip('[]').replace(' ', '').replace('\n', '')

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self._length

    def __iter__(self):
        return self._string.__iter__()

    def __int__(self):
        return self.value

    def __eq__(self, value):
        return self.value == int(value)

    def __gt__(self, value):
        return self.value > int(value)

    def __lt__(self, value):
        return self.value < int(value)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start_i, stop_i = key.start, key.stop
            if start_i is None:
                start_i = 0
            if stop_i is None:
                stop_i = self._length

            sliced_string = self._string[key]

            return BitString(int(str(sliced_string).strip(
                '[]').replace(' ', ''), base=2), length=(stop_i-start_i))
        return self._string.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(value, BitString):
            value = value._string
        return self._string.__setitem__(key, value)

    def __or__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=int)
        return self._string.__or__(value._string)

    def __ior__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=int)
        return self._string.__ior__(value._string)

    def __and__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=int)
        return self._string.__and__(value._string)

    def __iand__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=value)
        return self._string.__iand__(value._string)

    def __xor__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=int)
        return self._string.__xor__(value._string)

    def __ixor__(self, value):
        if isinstance(value, int):
            value: BitString = BitString(value=int)
        return self._string.__ixor__(value._string)

    def __rshift__(self, value):
        if isinstance(value, int):
            string = self._string.copy()
            string[value:] = string[:self._length-value]
            string[:value] &= 0
            shifted_string = BitString(length=len(string))
            shifted_string._string = string
            shifted_string._sign = self._sign
            return shifted_string
        raise ValueError("Shift amount must be integer.")

    def __ilshift__(self, value):
        if isinstance(value, int):
            self._string[value:] = self._string[:-value]
            self._string[:value] &= 0
            return self
        raise ValueError("Shift amount must be integer.")

    def __lshift__(self, value):
        if value == 0:
            return self._string.copy()
        if isinstance(value, int):
            string = self._string.copy()
            string[:-value] = string[value:]
            string[-value:] &= 0
            shifted_string = BitString(length=len(string))
            shifted_string._string = string
            shifted_string._sign = self._sign
            return shifted_string
        raise ValueError("Shift amount must be integer.")

    def __irshift__(self, value):
        if isinstance(value, int):
            self._string[:-value] = self._string[value:]
            self._string[-value:] &= 0
            return self
        raise ValueError("Shift amount must be integer.")

    # PROPERTIES #
    @property
    def value(self) -> int:
        return int(self.__str__(), base=2)

    @value.setter
    def value(self, raw_value) -> None:
        if not raw_value:
            self._sign = 0
            self._string: np.ndarray = np.zeros(
                (self._length,), dtype=np.uint8)
        else:
            self._sign = 1
            value = raw_value % (2**self._length - 1)
            if raw_value < 0:
                self._sign = -1
                value += 1
            bin_str = bin(value)[2:]
            self._string: np.ndarray = np.array(
                list('0'*(self._length-len(bin_str)) + bin_str), dtype=np.uint8)

    @property
    def signedValue(self) -> int:
        if self._sign >= 0:
            return self.value
        return -(2**self._length % self.value)

    # PUBLIC METHODS #

    # PRIVATE METHODS #


class Register(BitString):

    # STATIC VARIABLES #

    # DUNDERS #
    def __init__(self, register_id, value=0):
        super().__init__(value=value, length=16)
        self.register_id = register_id

    # PROPERTIES #

    # PUBLIC METHODS #
    def setRegisterValue(self, value):
        """ Overwrites all bits. """
        self.value = value

    def getBinID(self) -> str:
        return bin(self.register_id)[2:]

    # PRIVATE METHODS #


class _Instruction(object):

    # STATIC VARIABLES #

    # DUNDERS #
    def __init__(self, **fractions):
        super().__init__()
        self.fractions = fractions

    # PROPERTIES #

    # PUBLIC METHODS #
    def toMachineCode(self) -> str:
        res = ""
        for i, fraction in enumerate(self.fractions.values()):
            if isinstance(fraction, Register):
                fraction = fraction.register_id
            if fraction and fraction < 0:
                fraction = 2**self.field_bit_lengths[i] + fraction
            if fraction is None:
                fraction_bits = bin(2**self.field_bit_lengths[i])[3:]
            else:
                fraction_bits = bin(fraction)[2:]
            res += '0' * \
                (self.field_bit_lengths[i]-len(fraction_bits)) + fraction_bits
        return res

    # PRIVATE METHODS #


class R_Type(_Instruction):

    # STATIC VARIABLES #
    field_bit_lengths = [4, 1, 3, 3, 5]

    # DUNDERS #
    def __init__(self, **fractions):
        fracs = {opc: None, ctrl: None, rs: None, rt: None, fun: None}
        fracs.update(fractions)
        super().__init__(**fracs)

    # PROPERTIES #

    # PUBLIC METHODS #

    # PRIVATE METHODS #


class I_Type(_Instruction):

    # STATIC VARIABLES #
    field_bit_lengths = [4, 1, 3, 8]

    # DUNDERS #
    def __init__(self, **fractions):
        fracs = {opc: None, ctrl: None, rs: None, imm: None}
        fracs.update(fractions)
        super().__init__(**fracs)

    # PROPERTIES #

    # PUBLIC METHODS #

    # PRIVATE METHODS #
