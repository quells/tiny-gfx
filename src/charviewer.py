from nmigen import *
from nmigen.build import *

from charmap import CharMap
from vga_bus import VGABus

class CharViewer(Elaboratable):
    def __init__(self, vga: VGABus, charmap: CharMap):
        self.src = vga
        self.vga = VGABus(vga.timing)

        self.charmap = charmap
        self.char = Signal(8)
        self.mask = Signal(8)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        self.vga.forward(m, self.src)

        out = Signal()
        m.d.comb += [
            out.eq((self.mask & self.charmap.data) != 0),
        ]

        m.d.px += [
            # Jank - charmap slow, so need to offset by a pixel
            self.mask.eq(1 << (self.src.x-1)[0:3]),
            self.char.eq((self.src.y[3:7] << 4) | self.src.x[3:7]),
            self.charmap.char.eq(self.char),
            self.charmap.line.eq(self.src.y[0:3]),
            self.vga.r.eq(out),
            self.vga.g.eq(out),
            self.vga.b.eq(out),
        ]

        return m
