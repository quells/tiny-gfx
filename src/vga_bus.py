from nmigen import *
from nmigen.hdl.rec import *

from utils import bitcount
from vga_timing import VGATiming

class VGALayout(Layout):
    def __init__(self, w: int, h: int, h_px: int, v_lines: int):
        super().__init__([
            ("hsync", 1),
            ("vsync", 1),
            ("visible", 1),
            ("x", bitcount(w)),
            ("y", bitcount(h)),
            ("_x", bitcount(h_px)),
            ("_y", bitcount(v_lines)),
            ("r", 1),
            ("g", 1),
            ("b", 1),
        ])

class VGABus(Record):
    def __init__(self, t: VGATiming):
        layout = VGALayout(t.vx, t.vy, t.h_px, t.v_lines)
        super().__init__(layout)
        self.timing = t

    def forward(self, m: Module, src):
        m.d.comb += [
            self.hsync.eq(src.hsync),
            self.vsync.eq(src.vsync),
            self.visible.eq(src.visible),
        ]
        m.d.px += [
            self.x.eq(src.x),
            self.y.eq(src.y),
            self._x.eq(src._x),
            self._y.eq(src._y),
            self.r.eq(src.r),
            self.g.eq(src.g),
            self.b.eq(src.b),
        ]
