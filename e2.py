from pymtl3 import *


class FullAdderGL(Component):
    def construct(s):
        s.a = InPort()
        s.b = InPort()
        s.cin = InPort()

        s.sum = OutPort()
        s.cout = OutPort()

        @update
        def upblk():
            s.sum @= s.a ^ s.b ^ s.cin
            s.cout @= ((s.a ^ s.b) &
                                s.cin) | (s.a & s.b)


if __name__ == "__main__":
    adder = FullAdderGL()
    adder.apply(DefaultPassGroup(textwave=True))
    adder.sim_reset()

    adder.a @= 1
    adder.b @= 1
    adder.cin @= 1
    adder.sim_tick()
    adder.a @= 0
    adder.b @= 1
    adder.cin @= 1
    adder.sim_tick()
    adder.sim_tick()
    adder.print_textwave()
