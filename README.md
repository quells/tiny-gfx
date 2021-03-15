# Tiny GFX

A simple "graphics card" with VGA output built on the TinyFPGA platform.

## Build and Flash

Requires nMigen and its icestorm40 dependencies.

```
$ python3 gfx.py
$ tinyprog -p build/top.bin
```

## Acknowledgements

PLL generation and basic VGA setup: https://github.com/juanmard/screen-pong

nMigen reference: https://github.com/RobertBaruch/nmigen-tutorial
