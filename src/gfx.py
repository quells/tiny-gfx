from nmigen import *
from nmigen.build import *
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform

from pixel_clock import PixelClock
from vga import VGA
from vga_timing import *

from checkerboard import Checkerboard
from charmap import CharMap
from charviewer import CharViewer
from text_buffer import TextBuffer
from text_mode import TextMode

class Gfx(Elaboratable):
    def __init__(self, timings: VGATiming):
        self.timings = timings
    
    def _generate_domain_clocks(self, m: Module):
        """
        px    - Pixel clock for VGA.
        sync  - General purpose system clock. Tied to px PLL input.
        """
        px = PixelClock(self.timings.px_clk)
        m.submodules += px
        m.domains.px = px.domain

        clk_pin = ClockSignal("sync")
        m.d.comb += px.clk_pin.eq(clk_pin)
    
    def elaborate(self, platform: Platform):
        m = Module()
        self._generate_domain_clocks(m)

        # VGA clock generator
        vga = VGA(self.timings)
        m.submodules += vga

        # Text Memory Blocks
        charmap = CharMap("data/elkgrove.json")
        m.submodules += charmap
        # charviewer = CharViewer(vga.bus, charmap)
        # m.submodules += charviewer
        textbuf = TextBuffer(self.timings.vx // 8, self.timings.vy // 8)
        m.submodules += textbuf

        textmode = TextMode(vga.bus, charmap, textbuf)
        m.submodules += textmode

        # Hook up external pins

        # VGA
        vga_out = textmode.vga
        m.d.comb += [
            platform.request("pin_13").o.eq(vga_out.hsync),
            platform.request("pin_12").o.eq(vga_out.vsync),
        ]
        m.d.px += [
            platform.request("pin_11").o.eq(vga_out.visible & vga_out.b),
            platform.request("pin_10").o.eq(vga_out.visible & vga_out.g),
            platform.request("pin_09").o.eq(vga_out.visible & vga_out.r),
        ]

        return m

if __name__ == "__main__":
    platform = TinyFPGABXPlatform()

    print("Defining pins")
    platform.add_resources([
        # VGA
        Resource("pin_09", 0, Pins("E1", dir="o")),
        Resource("pin_10", 0, Pins("G2", dir="o")),
        Resource("pin_11", 0, Pins("H1", dir="o")),
        Resource("pin_12", 0, Pins("J1", dir="o")),
        Resource("pin_13", 0, Pins("H2", dir="o")),
    ])

    print("Creating Gfx module")
    m = Gfx(VGA_640_480_60)

    print("Building")
    platform.build(m, do_program=False)
