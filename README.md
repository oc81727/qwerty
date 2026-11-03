# qwerty
QR code generator.

Example usage:
```python
import gen
target = "youtu.be/dQw4w9WgXcQ"
version = 2
# 1, 2, 3, 4, 5

corLvl = "L"
# "L", "M", "Q", "H"

g = gen.gen(target, version, corLvl)
g.output(inverse = False) # inverts colors of qr code. use False if terminal has a dark background, True if not



```
