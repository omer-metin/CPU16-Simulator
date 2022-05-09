from common.definitions import *
from common.types import *
from engine.hardware.components import InstructionMemory, Memory, Registers


rd = Registers.getRegister('rd')


def fnc_add(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue + rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_and(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue & rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_div(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue // rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_mult(ctrl: int, rs: Register, rt: Register):
    val = rt.signedValue * rs.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_nor(ctrl: int, rs: Register, rt: Register):
    val = ~(rs.signedValue | rt.signedValue)
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_or(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue | rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_slt(ctrl: int, rs: Register, rt: Register):
    val = 1 if rs.signedValue < rt.signedValue else 0
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_sub(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue - rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


def fnc_xor(ctrl: int, rs: Register, rt: Register):
    val = rs.signedValue ^ rt.signedValue
    if ctrl:
        rd_old = rd.signedValue
        rd.setRegisterValue(val)
        return ([(rd.register_id, rd_old)], [])
    else:
        rt_old = rt.signedValue
        rt.setRegisterValue(val)
        return ([(rt.register_id, rt_old)], [])


# I Type Start #
def fnc_muli(rs: Register, imm):
    val = rs.signedValue * imm
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_slti(rs: Register, imm):
    val = 1 if rs.signedValue < imm else 0
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_lui(imm):
    val = (BitString(imm) << 8).signedValue
    print(val)
    print(BitString(imm))
    print(BitString(imm) << 8)
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    print(rd)
    return ([(rd.register_id, rd_old)], [])


def fnc_sll(rs: Register, rs_sa):
    sa = rs_sa.value if isinstance(rs_sa, Register) else rs_sa
    val = rs.value << sa
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_srl(rs: Register, rs_sa):
    sa = rs_sa.value if isinstance(rs_sa, Register) else rs_sa
    val = rs.value >> sa
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_lw(rs: Register, imm):
    val = Memory.loadWord(rs.value, offset=imm)
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_sw(rs: Register, imm):
    val = rd.value
    mem1_old = Memory.loadByte(rs.value, offset=imm)
    mem2_old = Memory.loadByte(rs.value, offset=imm+1)
    Memory.storeWord(rs.value, offset=imm, value=val)
    return ([], [(rs.value + imm, mem1_old), (rs.value + imm + 1, mem2_old)])


def fnc_beq(rs: Register, imm):
    if rs.signedValue == rd.signedValue:
        InstructionMemory.PC += imm
    return ([], [])


def fnc_bne(rs: Register, imm):
    if rs.signedValue != rd.signedValue:
        InstructionMemory.PC += imm
    return ([], [])


def fnc_j(tgt):
    InstructionMemory.PC = tgt
    return ([], [])


def fnc_jr(rs: Register):
    InstructionMemory.PC = rs.value
    return ([], [])


def fnc_jal(tgt):
    ra_old = Registers.getRegister('ra').signedValue
    Registers.getRegister('ra').setRegisterValue(InstructionMemory.PC)
    InstructionMemory.PC = tgt
    return ([(Registers.getRegister('ra').register_id, ra_old)], [])


def fnc_ori(rs: Register, imm):
    val = rs.signedValue | imm
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


def fnc_addi(rs: Register, imm):
    val = rs.signedValue + imm
    rd_old = rd.signedValue
    rd.setRegisterValue(val)
    return ([(rd.register_id, rd_old)], [])


instruction_functions = {
    add_: fnc_add,
    addu_: fnc_add,
    and_: fnc_and,
    div_: fnc_div,
    divu_: fnc_div,
    mult_: fnc_mult,
    multu_: fnc_mult,
    nor_: fnc_nor,
    or_: fnc_or,
    sllv_: fnc_sll,
    slt_: fnc_slt,
    sltu_: fnc_slt,
    srlv_: fnc_srl,
    sub_: fnc_sub,
    subu_: fnc_sub,
    xor_: fnc_xor,

    muli_: fnc_muli,
    slti_: fnc_slti,
    lui_: fnc_lui,
    sll_: fnc_sll,
    srl_: fnc_srl,
    lw_: fnc_lw,
    sw_: fnc_sw,
    beq_: fnc_beq,
    bne_: fnc_bne,
    j_: fnc_j,
    jr_: fnc_jr,
    jal_: fnc_jal,
    addi_: fnc_addi,
    ori_: fnc_ori
}
