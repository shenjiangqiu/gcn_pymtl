
from pymtl3 import *
from pymtl3.datatypes.bitstructs import mk_bitstruct
from pymtl3.dsl.Connectable import Wire

from pymtl3.stdlib.mem import MemMasterIfcRTL, MemMinionIfcRTL

req_type = mk_bitstruct("request", {"addr": b4})
resp_type = mk_bitstruct("resp", {"data": b4})


class Master(Component):
    def construct(s):
        s.ifc = MemMasterIfcRTL(req_type, resp_type)
        s.reg = Wire(4)

        @update
        def update_comb():
            if s.ifc.req.rdy:
                s.ifc.req.en@=1
                s.ifc.req.addr@=s.reg

        @update_ff
        def update_edge():
            if s.reset:
                s.reg <<= 0
            # when will send this requst, add the req by 1
            if s.ifc.req.rdy:
                s.reg <<= s.reg+1


class Minor(Component):
    def construct(s):
        s.ifc = MemMinionIfcRTL(req_type, resp_type)
        s.data = Wire(4)

        @update
        def update_comb():
            # req always ready
            s.ifc.rdy@=1

            # response the addr +2
            if s.ifc.req.en:
                s.ifc.resp.rdy@=1
                s.ifc.resp.data@=s.ifc.req.addr+2


class Harness(Component):
    def construct(s):
        s.mas = Master()
        s.min = Minor()
        s.mas.ifc //= s.min.ifc


if __name__ == "__main__":
    eq = Harness()
    eq.apply(DefaultPassGroup())
    eq.sim_reset()
