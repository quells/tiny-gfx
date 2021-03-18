import warnings

from nmigen import *
from nmigen.lib.cdc import ResetSynchronizer

def _calc_freq_coefficients(fin: int, freq: float):
    assert 10 <= fin <= 16
    assert 16 <= freq <= 275
    divr_range = 16
    divf_range = 128
    fout = 0
    best_fout = float("inf")
    best = None
    for divr in range(divr_range):
        pfd = fin / (divr + 1)
        if 10 <= pfd <= 133:
            for divf in range(divf_range):
                vco = pfd * (divf + 1)
                if 533 <= vco <= 1066:
                    for divq in range(1, 7):
                        fout = vco * 2**-divq
                        if abs(fout - freq) < abs(best_fout - freq):
                            best_fout = fout
                            best = (divr, divf, divq)
    if best_fout != freq:
        warnings.warn(
            f"PLL: requested {freq} MHz, got {best_fout} MHz",
            stacklevel=3
        )
    return best

class PixelClock(Elaboratable):
    def __init__(self, freq_out: float, freq_in: int = 16):
        coeff = _calc_freq_coefficients(freq_in, freq_out)
        if not coeff:
            raise Exception("could not calculate PLL coefficients")
        self.divr = coeff[0]
        self.divf = coeff[1]
        self.divq = coeff[2]
        
        self.clk_pin = Signal()
        self.domain = ClockDomain("px")
        self.ports = [
            self.clk_pin,
            self.domain.clk,
            self.domain.rst,
        ]

    def elaborate(self, platform):
        pll_lock = Signal()
        pll = Instance(
            "SB_PLL40_CORE",
            p_FEEDBACK_PATH="SIMPLE",
            p_PLLOUT_SELECT="GENCLK",
            p_DIVR=self.divr,
            p_DIVF=self.divf,
            p_DIVQ=self.divq,
            p_FILTER_RANGE=0b001,

            i_REFERENCECLK=self.clk_pin,
            i_RESETB=Const(1),
            i_BYPASS=Const(0),

            o_PLLOUTCORE=ClockSignal("px"),
            o_LOCK=pll_lock,
        )

        rs = ResetSynchronizer(~pll_lock, domain="px")

        m = Module()
        m.submodules += [pll, rs]
        return m
