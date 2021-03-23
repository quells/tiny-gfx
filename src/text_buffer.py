from nmigen import *
from nmigen.build import *

from utils import bitcount

class TextBuffer(Elaboratable):
    def __init__(self, width: int, height: int):
        """
        width: width in characters
        height: height in characters
        """
        self.w = w = bitcount(width)
        self.h = h = bitcount(height)
        self.i = Signal(w)
        self.j = Signal(h)

        self.addr = Signal(w + h)
        self.data_r = Signal(8)
        self.data_w = Signal(8)
        self.we = Signal()
        self.text = Memory(width=8, depth=width*height, init=[ord(c) for c in "Loading..."])

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        m.submodules.rdport = rdport = self.text.read_port()
        m.submodules.wrport = wrport = self.text.write_port()
        m.d.comb += [
            # Update address for (i, j)
            self.addr.eq((self.j * self.w) + self.i),

            # Load old value into data_r
            rdport.addr.eq(self.addr),
            self.data_r.eq(rdport.data),

            # If write enabled (we), write new value from data_w into memory
            wrport.addr.eq(self.addr),
            wrport.data.eq(self.data_w),
            wrport.en.eq(self.we),
        ]

        return m

    def ports(self):
        return [
            self.i,
            self.j,
            self.data_r,
            self.data_w,
            self.we,
        ]
