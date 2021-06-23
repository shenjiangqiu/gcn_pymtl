import pymtl3
from pymtl3 import *


class Adder(Component):
    def construct(s):
        s._in1 = InPort()
        s._in2 = InPort()
        s._in_over_flow = InPort()

        s._out = OutPort()
        s._out_overflow = OutPort()

        @update
        def update_comb():
            s._out @= s._in1 ^ s._in2 ^ s._in_over_flow
            s._out_overflow @= ((s._in1 ^ s._in2) & s._in_over_flow) | (s._in1 & s._in2)


if __name__ == "__main__":
    adder = Adder()
    adder.apply(DefaultPassGroup(textwave=True))
    adder.sim_reset()

    adder._in1 @= 1
    adder._in2 @= 1
    adder._in_over_flow @= 1
    adder.sim_tick()
    adder._in1 @= 0
    adder._in2 @= 1
    adder._in_over_flow @= 1
    adder.sim_tick()
    adder.sim_tick()
    adder.print_textwave()
