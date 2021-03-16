from nmigen import *
from nmigen.build import *

from vga_bus import VGABus

class Checkerboard(Elaboratable):
    def __init__(self, vga: VGABus):
        self.src = vga
        self.vga = VGABus(vga.timing)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        self.vga.forward(m, self.src)
        m.d.comb += self.vga.visible.eq(Mux(
            self.src.x[0] ^ self.src.y[0],
            1,
            0,
        ))

        return m
