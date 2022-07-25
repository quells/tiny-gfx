from nmigen import *
from nmigen.build import *

from utils import bitcount
from vga_bus import VGABus

class SpriteEngine(Elaboratable):
    def __init__(self, vga: VGABus):
        self.src = vga
        self.vga = VGABus(vga.timing)

        self.x = Signal(bitcount(vga.timing.h_px))
        self.y = Signal(bitcount(vga.timing.v_lines))

        # bitmap = [0x55,0xaa,0x55,0xaa,0x55,0xaa,0x55,0xaa]
        bitmap = [0x3c,0x7e,0xff,0xff,0xff,0xff,0x7e,0x3c]
        self.mem = Memory(width=8, depth=8, init=bitmap)
        self.char = Signal(8)
        self.mask = Signal(8)
    
    def elaborate(self, platform: Platform) -> Module:
        m = Module()

        m.submodules.rdport = rdport = self.mem.read_port()
        addr = Signal(3)
        m.d.comb += [
            rdport.addr.eq(addr),
            self.char.eq(rdport.data),
        ]

        self.vga.forward(m, self.src)

        vx = self.vga._x - 1
        inside_sprite_x = (self.x <= vx) & (vx <= (self.x + 8))
        inside_sprite_y = (self.y <= self.vga._y) & (self.vga._y < (self.y + 8))

        with m.If(inside_sprite_y):
            m.d.px += addr.eq(self.vga.y - self.y)

        with m.If(inside_sprite_x & inside_sprite_y):
            m.d.px += self.mask.eq(1 << (vx - self.x))
        with m.Else():
            m.d.px += self.mask.eq(0)

        out = Signal()
        m.d.comb += [
            out.eq((self.mask & self.char) != 0),
        ]

        with m.If(inside_sprite_x & inside_sprite_y):
            m.d.px += [
                self.vga.r.eq(out),
                self.vga.g.eq(out),
                self.vga.b.eq(out),
            ]

        return m

    def ports(self):
        return [
            self.x,
            self.y,
        ]
