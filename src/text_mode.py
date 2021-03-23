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

        char_idx = Signal(8)
        char_data = Signal(8)
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
            """
            FIXME
            Load addr into textbuf
            Read char code from textbuf
            Load addr (char code + line) into charmap
            Read char row from charmap
            Load addr into linebuf
            Write char row to linebuf
            """
            with m.Switch(self.src.hblank % 6):
                with m.Case(0):
                    m.d.px += [
                        # 1 Load addr into textbuf
                        self.textbuf.i.eq((self.src.hblank >> 1) % self.textbuf.w),
                        self.textbuf.j.eq(self.src.nexty[0:3]),
                    ]
                with m.Case(1):
                    m.d.px += [
                        # 2 Read char from textbuf
                        char_idx.eq(self.textbuf.data_r),
                    ]
                with m.Case(2):
                    m.d.px += [
                        # 3 Load addr into charmap
                        self.charmap.char.eq(char_idx),
                        self.charmap.line.eq(self.src.nexty[0:3]),
                    ]
                with m.Case(3):
                    m.d.px += [
                        # 4 Read char row from charmap
                        char_data.eq(self.charmap.data),
                    ]
                with m.Case(4):
                    m.d.px += [
                        # 5 Load addr into linebuf
                        self.linebuf.addr.eq((self.src.hblank >> 1) % self.textbuf.w),
                    ]
                with m.Case(5):
                    m.d.px += [
                        # 6 Write char row to linebuf
                        self.linebuf.data_w.eq(char_data),
                    ]

        return m
