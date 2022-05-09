# R Types #
add_ = 'add'
addu_ = 'addu'
and_ = 'and'
div_ = 'div'
divu_ = 'divu'
mult_ = 'mult'
multu_ = 'multu'
nor_ = 'nor'
or_ = 'or'
sllv_ = 'sllv'
slt_ = 'slt'
sltu_ = 'sltu'
srlv_ = 'srlv'
sub_ = 'sub'
subu_ = 'subu'
xor_ = 'xor'

# I Types #
muli_ = 'muli'
slti_ = 'slti'
lui_ = 'lui'
sll_ = 'sll'
srl_ = 'srl'
lw_ = 'lw'
sw_ = 'sw'
beq_ = 'beq'
bne_ = 'bne'
j_ = 'j'
jr_ = 'jr'
jal_ = 'jal'
addi_ = 'addi'
ori_ = 'ori'

# J Types #

opcodes = dict([
    # R Types #
    (add_,      0b1000),
    (addu_,     0b1000),
    (and_,      0b1000),
    (div_,      0b1000),
    (divu_,     0b1000),
    (mult_,     0b1000),
    (multu_,    0b1000),
    (nor_,      0b1000),
    (or_,       0b1000),
    (sllv_,     0b1000),
    (slt_,      0b1000),
    (sltu_,     0b1000),
    (srlv_,     0b1000),
    (sub_,      0b1000),
    (subu_,     0b1000),
    (xor_,      0b1000),
    # I Types #
    (muli_,     0b1101),
    (slti_,     0b1100),
    (lui_,      0b1110),
    (sll_,      0b1010),
    (srl_,      0b0110),
    (lw_,       0b1111),
    (sw_,       0b0011),
    (beq_,      0b0000),
    (bne_,      0b0000),
    (j_,        0b0001),
    (jr_,       0b0001),
    (jal_,      0b1001),
    (addi_,     0b1011),
    (ori_,      0b0101)
])


rs = 'rs'
rt = 'rt'
imm = 'immediate'
fun = 'funct'
opc = 'opcode'
ctrl = 'control'

instruction_machinecode_orders = dict([
    (add_,      {opc: opcodes[add_], ctrl:1, fun: 0b00_000}),
    (addu_,     {opc: opcodes[addu_], ctrl:1, fun: 0b00_001}),
    (and_,      {opc: opcodes[and_], ctrl:1, fun: 0b00_010}),
    (div_,      {opc: opcodes[div_], ctrl:1, fun: 0b00_011}),
    (divu_,     {opc: opcodes[divu_], ctrl:1, fun: 0b00_100}),
    (mult_,     {opc: opcodes[mult_], ctrl:1, fun: 0b00_101}),
    (multu_,    {opc: opcodes[multu_], ctrl:1, fun: 0b00_110}),
    (nor_,      {opc: opcodes[nor_], ctrl:1, fun: 0b00_111}),
    (or_,       {opc: opcodes[or_], ctrl:1, fun: 0b01_000}),
    (sllv_,     {opc: opcodes[sllv_], ctrl:1, fun: 0b01_001}),
    (slt_,      {opc: opcodes[slt_], ctrl:1, fun: 0b01_010}),
    (sltu_,     {opc: opcodes[sltu_], ctrl:1, fun: 0b01_011}),
    (srlv_,     {opc: opcodes[srlv_], ctrl:1, fun: 0b01_100}),
    (sub_,      {opc: opcodes[sub_], ctrl:1, fun: 0b01_101}),
    (subu_,     {opc: opcodes[subu_], ctrl:1, fun: 0b01_110}),
    (xor_,      {opc: opcodes[xor_], ctrl:1, fun: 0b01_111}),

    (muli_,     {opc: opcodes[muli_], ctrl: 1}),
    (slti_,     {opc: opcodes[slti_], ctrl: 1}),
    (lui_,      {opc: opcodes[lui_], ctrl: 1}),
    (sll_,      {opc: opcodes[sll_], ctrl: 1}),
    (srl_,      {opc: opcodes[srl_], ctrl: 1}),
    (lw_,       {opc: opcodes[lw_], ctrl: 1}),
    (sw_,       {opc: opcodes[sw_], ctrl: 1}),
    (beq_,      {opc: opcodes[beq_], ctrl: 0}),
    (bne_,      {opc: opcodes[bne_], ctrl: 1}),
    (j_,        {opc: opcodes[j_], ctrl: 0}),
    (jr_,       {opc: opcodes[jr_], ctrl: 1}),
    (jal_,      {opc: opcodes[jal_], ctrl: 1}),
    (addi_,     {opc: opcodes[addi_], ctrl: 1}),
    (ori_,      {opc: opcodes[ori_], ctrl: 1})
])

instruction_assembly_orders = dict([
    (add_,      [opc, ctrl, rs, rt, fun]),
    (addu_,     [opc, ctrl, rs, rt, fun]),
    (and_,      [opc, ctrl, rs, rt, fun]),
    (div_,      [opc, ctrl, rs, rt, fun]),
    (divu_,     [opc, ctrl, rs, rt, fun]),
    (jr_,       [opc, ctrl, rs, fun]),
    (mult_,     [opc, ctrl, rs, rt, fun]),
    (multu_,    [opc, ctrl, rs, rt, fun]),
    (nor_,      [opc, ctrl, rs, rt, fun]),
    (or_,       [opc, ctrl, rs, rt, fun]),
    (sllv_,     [opc, ctrl, rt, rs, fun]),
    (slt_,      [opc, ctrl, rs, rt, fun]),
    (sltu_,     [opc, ctrl, rs, rt, fun]),
    (srlv_,     [opc, ctrl, rt, rs, fun]),
    (sub_,      [opc, ctrl, rs, rt, fun]),
    (subu_,     [opc, ctrl, rs, rt, fun]),
    (xor_,      [opc, ctrl, rs, rt, fun]),

    (muli_,     [opc, rs, imm]),
    (slti_,     [opc, rs, imm]),
    (lui_,      [opc, imm]),
    (sll_,      [opc, rs, imm]),
    (srl_,      [opc, rs, imm]),
    (lw_,       [opc, rs, imm]),
    (sw_,       [opc, rs, imm]),
    (beq_,      [opc, rs, imm]),
    (bne_,      [opc, rs, imm]),
    (j_,        [opc, imm]),
    (jr_,       [opc, rs]),
    (jal_,      [opc, imm]),
    (addi_,     [opc, rs, imm]),
    (ori_,      [opc, rs, imm])

])
