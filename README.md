# qwerty


QR code generator.

Example usage:
```python
import gen
target = "youtu.be/dQw4w9WgXcQ"
version = 2
# 1, 2, 3, 4, 5
# higher versions are larger and have higher capacities.

corLvl = "L"
# "L", "M", "Q", "H"
# error correction levels: Low, Medium, Quarter, High

g = gen.gen(target, version, corLvl)
g.output(inverse = False) # inverts colors of qr code. use False if terminal has a dark background, True if not

g.pad(1) # adds padding around the generated code
g.output(padded=True)



```

<img width="367" height="394" alt="image" src="https://github.com/user-attachments/assets/fd0c8894-a1e6-4221-bc1f-2405813b5f37" />
