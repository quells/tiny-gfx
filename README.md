# Tiny GFX

A simple "graphics card" with VGA output built on the TinyFPGA platform.

## Build and Flash

Requires nMigen and its icestorm40 dependencies.

```
$ python3 src/gfx.py
$ tinyprog -p build/top.bin
```

or just `make flash`

## Acknowledgements

PLL generation and basic VGA setup: https://github.com/juanmard/screen-pong

nMigen reference: https://github.com/RobertBaruch/nmigen-tutorial

Elkgrove bitmap font created using [vga-font](https://github.com/quells/vga-font/) and based on the [Chicago typeface](https://en.wikipedia.org/wiki/Chicago_(typeface))
