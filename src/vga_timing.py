
class VGATiming(object):
    """
    VGA timing parameters.

    Args:
        px_clk: Pixel clock frequency (MHz)

        vx:  visible width (px)
        hfp: horizontal front porch (px)
        hsp: horizontal sync pulse (px)
        hbp: horizontal back porch (px)

        vy:  visible height (lines)
        vfp: vertical front porch (lines)
        vsp: vertical sync pulse (lines)
        vbp: vertical back porch (lines)
    """
    def __init__(self, px_clk: float, vx: int, hfp: int, hsp: int, hbp: int, vy: int, vfp: int, vsp: int, vbp: int):
        self.px_clk = px_clk

        self.vx = vx
        self.hfp = hfp
        self.hsp = hsp
        self.hbp = hbp
        self.hblank = hfp + hsp + hbp
        self.h_px = vx + self.hblank
        self.hsync = (vx + hfp, vx + hfp + hsp)

        self.vy = vy
        self.vfp = vfp
        self.vsp = vsp
        self.vbp = vbp
        self.v_lines = vy + vfp + vsp + vbp
        self.vsync = (vy + vfp, vy + vfp + vsp)

VGA_640_480_60 = VGATiming(
    # Technically 25.175 MHz but that's unattainable and most monitors will accept this.
    25.0,
    640, 16, 96, 48,
    480, 10, 2, 33,
)

VESA_640_480_75 = VGATiming(
    31.5,
    640, 16, 64, 120,
    480, 1, 3, 16,
)

SVGA_800_600_60 = VGATiming(
    40.0,
    800, 40, 128, 88,
    600, 1, 4, 23,
)
