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
        domain_name: str = "px",
    ):
        self.timing = timing
        self.domain_name = domain_name

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

        # Increment horizontal counter
        with m.If(self.h < self.timing.h_px-1):
            m.d[self.domain_name] += self.h.eq(self.h + 1)
        with m.Else():
            # At end of line, reset horizontal counter
            m.d[self.domain_name] += self.h.eq(0)
            # ... and increment vertical counter or reset it at end of frame.
            m.d[self.domain_name] += self.v.eq(
                Mux(self.v < (self.timing.v_lines-1),
                self.v+1,
                0)
            )

        # Sync pulses (active low)
        m.d.comb += self.bus.hsync.eq(~((self.timing.hsync_start < self.h) & (self.h < self.timing.hsync_end)))
        m.d.comb += self.bus.vsync.eq(~((self.timing.vsync_start < self.v) & (self.v < self.timing.vsync_end)))

        # Visible region
        m.d.comb += self.bus.visible.eq((self.h < self.timing.vx) & (self.v < self.timing.vy))

        # Update pixel positions
        m.d[self.domain_name] += self.bus.x.eq(Mux(self.bus.visible, self.h, 0))
        m.d[self.domain_name] += self.bus.y.eq(Mux(self.bus.visible, self.v, 0))

        return m
