import json

from nmigen import *
from nmigen.build import *

class CharMap(Elaboratable):
    def __init__(self, filename: str):
        # Characters are 8x8 bitmaps stored in 8-byte chunks.
        # Each byte is a row, LSB on left side. Rows stored top-to-bottom.
        # A1, A2, A3, ... Z6, Z7, Z8
        with open(filename) as f:
            print("Loading character map")
            data = json.load(f)
        charmap = []
        for c in data:
            charmap += bytes.fromhex(c)

        self.char = Signal(8)
        self.line = Signal(3)

        self.addr = Signal(8 + 3)
        self.data = Signal(8)
        self.mem = Memory(width=8, depth=256*8, init=charmap)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        m.submodules.rdport = rdport = self.mem.read_port()
        m.d.comb += [
            self.addr.eq((self.char << 3) | self.line),
            rdport.addr.eq(self.addr),
            self.data.eq(rdport.data),
        ]

        return m

    def ports(self):
        return [
            self.char,
            self.line,
            self.data,
        ]
