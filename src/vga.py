from nmigen import *
from nmigen.build import *

from vga_timing import VGATiming
from vga_bus import VGABus
from utils import bitcount

class VGA(Elaboratable):
    """
    VGA clock generator.
    """
    def __init__(
        self, 
        timing: VGATiming,
    ):
        self.timing = timing

        # "Beam" pixel position
        self.h = Signal(bitcount(timing.h_px))
        self.v = Signal(bitcount(timing.v_lines))

        # HSync, VSync, Visible, X, Y
        self.bus = VGABus(timing)

        self.ports = [
            self.bus,
        ]

    def elaborate(self, platform: Platform) -> Module:
        m = Module()
        t = self.timing

        # Increment horizontal counter
        with m.If(self.h < t.h_px-1):
            m.d.px += self.h.eq(self.h + 1)
        with m.Else():
            # At end of line, reset horizontal counter
            m.d.px += self.h.eq(0)
            # ... and increment vertical counter or reset it at end of frame.
            m.d.px += self.v.eq(
                Mux(self.v < (t.v_lines-1),
                self.v+1,
                0)
            )

        # Sync pulses (active low)
        m.d.comb += self.bus.hsync.eq(~((t.hsync[0] < self.h) & (self.h < t.hsync[1])))
        m.d.comb += self.bus.vsync.eq(~((t.vsync[0] < self.v) & (self.v < t.vsync[1])))

        # Visible region
        m.d.comb += self.bus.visible.eq((self.h < t.vx) & (self.v < t.vy))

        # Update pixel positions
        m.d.px += self.bus.x.eq(Mux(self.bus.visible, self.h, 0))
        m.d.px += self.bus.y.eq(Mux(self.bus.visible, self.v, 0))

        return m
