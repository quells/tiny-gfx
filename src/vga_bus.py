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
            ("r", 1),
            ("g", 1),
            ("b", 1),
        ])

class VGABus(Record):
    def __init__(self, timing: VGATiming):
        layout = VGALayout(timing.vx, timing.vy)
        super().__init__(layout)
        self.timing = timing

    def forward(self, m: Module, src):
        m.d.comb += [
            self.hsync.eq(src.hsync),
            self.vsync.eq(src.vsync),
            self.visible.eq(src.visible),
        ]
        m.d.px += [
            self.x.eq(src.x),
            self.y.eq(src.y),
            self.r.eq(src.r),
            self.g.eq(src.g),
            self.b.eq(src.b),
        ]
