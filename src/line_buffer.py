from nmigen import *
from nmigen.build import *

from utils import bitcount

class LineBuffer(Elaboratable):
    def __init__(self, width: int):
        """
        width: width in characters
        """
        self.mask = Signal(8)
        self.out = Signal()

        self.addr = Signal(bitcount(width))
        self.data_r = Signal(8)
        self.data_w = Signal(8)
        self.we = Signal()
        self.mem = Memory(width=8, depth=width)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        m.submodules.rdport = rdport = self.mem.read_port()
        m.submodules.wrport = wrport = self.mem.write_port()
        m.d.comb += [
            # Load old value into data_r
            rdport.addr.eq(self.addr),
            self.data_r.eq(rdport.data),

            # If write enabled (we), write new value from data_w into memory
            wrport.addr.eq(self.addr),
            wrport.data.eq(self.data_w),
            wrport.en.eq(self.we),

            # Get current pixel value
            self.out.eq((self.mask & self.data_r) != 0),
        ]

        return m

    def ports(self):
        return [
            self.mask,
            self.out,
            self.addr,
            self.data_w,
            self.we,
        ]
