from nmigen import *
from nmigen.build import *

from utils import bitcount
from charmap import CharMap
from text_buffer import TextBuffer
from line_buffer import LineBuffer
from vga_bus import VGABus

class TextMode(Elaboratable):
    def __init__(self, vga: VGABus, charmap: CharMap, textbuf: TextBuffer):
        self.src = vga
        self.vga = VGABus(vga.timing)

        self.charmap = charmap
        self.textbuf = textbuf
        self.linebuf = LineBuffer(vga.timing.vx // 8)

    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        self.vga.forward(m, self.src)
        m.submodules += self.linebuf

        out = Signal()
        m.d.comb += [
            out.eq(self.linebuf.out),
            self.linebuf.we.eq(~self.src.visible),
        ]

        with m.If(self.src.visible):
            m.d.px += [
                # Update line buffer readout
                self.linebuf.mask.eq(1 << (self.src.x)[0:3]),
                self.linebuf.addr.eq(self.src.x[3:]),

                # Display VGA
                self.vga.r.eq(out),
                self.vga.g.eq(out),
                self.vga.b.eq(out),
            ]
        with m.Else():
            # TODO fill linebuf with next line from textbuf
            m.d.px += [
            ]

        return m
