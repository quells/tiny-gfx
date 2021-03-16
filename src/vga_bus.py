from nmigen import *
from nmigen.hdl.rec import *

from utils import bitcount
from vga_timing import VGATiming

class VGALayout(Layout):
    def __init__(self, w: int, h: int):
        super().__init__([
            ("hsync", 1),
            ("vsync", 1),
            ("visible", 1),
            ("x", bitcount(w)),
            ("y", bitcount(h)),
            ("r", 3),
            ("g", 3),
            ("b", 2),
        ])

class VGABus(Record):
    def __init__(self, timing: VGATiming):
        layout = VGALayout(timing.vx, timing.vy)
        super().__init__(layout)
        self.timing = timing

    def forward(self, m: Module, src):
        m.d.comb += self.hsync.eq(src.hsync)
        m.d.comb += self.vsync.eq(src.vsync)
        m.d.comb += self.visible.eq(src.visible)
        m.d.comb += self.x.eq(src.x)
        m.d.comb += self.y.eq(src.y)
        m.d.comb += self.r.eq(src.r)
        m.d.comb += self.g.eq(src.g)
        m.d.comb += self.b.eq(src.b)
