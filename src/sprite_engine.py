from nmigen import *
from nmigen.build import *

from utils import bitcount
from vga_bus import VGABus

class SpriteEngine(Elaboratable):
    def __init__(self, vga: VGABus):
        self.src = vga
        self.vga = VGABus(vga.timing)

        self.x = Signal(bitcount(vga.timing.vx))
        self.y = Signal(bitcount(vga.timing.vy))

        bitmap = [
            0b00111100,
            0b01100110,
            0b11000011,
            0b10000001,
            0b10000001,
            0b11000011,
            0b01100110,
            0b00111100,
        ]
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
            self.x.eq(10),
            self.y.eq(10),
        ]

        self.vga.forward(m, self.src)

        inside_sprite = (self.x <= self.vga.x) & (self.vga.x < (self.x + 8)) & \
                        (self.y <= self.vga.y) & (self.vga.y < (self.y + 8))

        with m.If(inside_sprite):
            m.d.px += [
                self.mask.eq(1 << (self.vga.x - self.x)),
                addr.eq(self.vga.y - self.y),
            ]
        with m.Else():
            m.d.px += self.mask.eq(0)

        out = Signal()
        m.d.comb += [
            out.eq((self.mask & self.char) != 0),
        ]

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
