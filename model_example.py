from engine.software.mipsAssembler import MIPSAssembler
from engine.hardware.components import BitString
code = """
        ori $zero 3
        andc $zero $r1
        addc $rd $r1
        ori $zero 1
        andc $zero $r2
        addc $rd $r2
loop:   slt $zero $r1
        bne $zero r1_low
        andc $r0 $r1 
        j end
r1_low: sub $zero $r2
        addc $rd $r1
        jal count
        j loop
count:  addc $r2 $r3
        jr $ra
end:   
"""

print(MIPSAssembler.assembly(code))
a = {1: 4, 2: 5, 3: 5}

print(list(a.keys()).index(1))
