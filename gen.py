
def charToBin(c, length = 8):
	return bin(ord(c))[2:].rjust(length,"0")

def intToBin(i, length = 8):
	return bin(i)[2:].rjust(length,"0")



def encode(data, targetLength): # target length in bytes
	# version 1-Q
	# targetLength = 104 # 13 * 8
	targetLength *= 8
	ret = ""
	mode = "0100"

	ret += mode + intToBin(len(data), 8) # ver 1 

	for char in data:
		ret += charToBin(char)

	ret += "0" * min(104 - len(ret), 4) # 0 padding

	ret += "0" * (len(ret) % 8) # making length a multiple of 8



	ret +=  (intToBin(236) + intToBin(17))* (int((targetLength - len(ret))/8 /2) + 1)
	ret = ret[:targetLength]



	return ret

def decode(data):
	data = data[12:]
	ret = ""
	for i in range(len(data)//8):
		ret+=chr(int(data[i*8:i*8+8],2))
	return ret


def splitChunks(s, size = 8):
	return [s[i:i+size] for i in range(0,len(s),size)]





def calcGalois():
	power = {}
	for i in range(256):
		if i == 0:
			p = 1
		else:
			p = 2 * power[i-1]
		if p > 255:
			p = p ^ 285
		power[i] = p

	del power[255]

	reverse = dict((v,k) for k,v in power.items())
	reverse[0] = 0
		
	return power, reverse



def gfMult(a, b):
	# a and b are normal numbers
	exp = asPower[a] + asPower[b]
	# print(asPower[a])
	if exp > 255:
		exp = exp ^ 285
	return fromPower[exp]

# print(gfMult(16, 32))

def gfAdd(a, b):
	# a and b are exponents
	return asPower[fromPower[a] ^ fromPower[b]]


# print(gfAdd(25,2))

# print(toGF[3])
# print(fromGF[3])
# print(fromPower[25])


def gfAdd(a, b):
	# a and b are alphas
	return asPower[fromPower[a] ^ fromPower[b]]

def multPoly(a, b):
	ret = {}
	for powerA, coeffA in a.items():
		for powerB, coeffB in b.items():
			np = powerA + powerB
			nc = (coeffA + coeffB)%255
			if not np in ret:
				ret[np] = nc
			else:
				ret[np] = gfAdd(ret[np], nc)
	return ret

# print(multPoly(multPoly(p1, p2), {0:2,1:0}))


def genCodeword(num):
	# p1 = {0:0, 1:0} # x^0*a^0 + x^1*a^0
	# p2 = {0:1, 1:0} # x^0*a^1 + x^1*a^0
	ret = {1:0, 0:0}
	for i in range(num-1):
		ret = multPoly(ret, {1:0, 0:i+1})
	return ret

def incPower(d, n):
	return {k+n: v for k,v in d.items()}

# print(genCodeword(10))



def dataToPoly(data):
	chunks = splitChunks(data)
	return {len(chunks)-n-1:int(i,2) for n,i in enumerate(chunks)}







#32x25 + 91x24 + 11x23 + 120x22 + 209x21 + 114x20 + 220x19 + 77x18 + 67x17 + 64x16 + 236x15 + 17x14 + 236x13 + 17x12 + 236x11 + 17x10
# poly = {25:32,24:91,23:11,22:120,21:209,20:114,19:220,18:77,17:67,16:64,15:236,14:17,13:236,12:17,11:236,10:17}



def coeffToPower(d):
	return {k:asPower[v] for k,v in d.items()}

def powerToCoeff(d):
	return {k:fromPower[v] for k,v in d.items()}

def addPower(d,n):
	return {k:(v+n)%255 for k,v in d.items()}

def polyXor(p1, p2):
	# if len(p1)!=len(p2):
	# 	raise Exception(f"not de same length frfr\np1: {p1}\np2:{p2}")

	if len(p1) > len(p2):
		longer = p1
		shorter = p2
	else:
		shorter = p1
		longer = p2

	return {k:(v^shorter[k] if (k in shorter) else v) for k,v in longer.items()}


def polyDivide(mes, genPow):
	# mes = poly
	# genPow = codeWord
	# print("starting divide!")
	# print(mes)
	oriGenPow = {k: v for k, v in genPow.items()}
	oriGen = powerToCoeff(oriGenPow)
	# print(genPow)
	# prepare message polynomial
	# add power (correction length)
	# make generator the same power

	# multiply generator by first term of message (alpha adding)

	genPow = addPower(genPow, asPower[mes[max(mes.keys())]])
	gen = powerToCoeff(genPow)
	# print(genPow)
	# print(gen)
	# xor with message


	res = polyXor(mes, gen)
	# print(res)
	del res[max(res.keys())]
	# print("removed leading")
	# print(res)
	# discard 0 term
	# --HERE--

	# [ repeat
	for i in range(len(mes.keys())-1):
		# print("ori gen pow")
		oriGenPow = incPower(oriGenPow, -1)
		# print(oriGenPow)
		genPow = addPower(oriGenPow, asPower[res[max(res.keys())]])
		gen = powerToCoeff(genPow)
		# print(genPow)
		# print(gen)
		# multiply generator by first term of xor
		res = polyXor(res, gen)
		del res[max(res.keys())]
		# print("removed leading")
		# print(res)
		# input()
	# xor with result from --HERE--
	# ]
	return res


# print(intToBin(poly[25]))

class Grid:
	"""
	0,0 is on top left
	"""
	patternData = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170]
}
	remainderBits = {
1:	0,
2:	7,
3:	7,
4:	7,
5:	7,
6:	7,
7:	0,
8:	0,
9:	0,
10:	0,
11:	0,
12:	0,
13:	0,
14:	3,
15:	3,
16:	3,
17:	3,
18:	3,
19:	3,
20:	3,
21:	4,
22:	4,
23:	4,
24:	4,
25:	4,
26:	4,
27:	4,
28:	3,
29:	3,
30:	3,
31:	3,
32:	3,
33:	3,
34:	3,
35:	0,
36:	0,
37:	0,
38:	0,
39:	0,
40:	0
}
	def __init__(self, size):
		self.size = size
		self.grid = [[None for h in range(size)] for i in range(size)]
		self.validMap = [[None for h in range(size)] for i in range(size)]

	def set(self, x, y, value = True):
		self.grid[y][x] = value

	def fillArea(self, x1, y1, x2, y2, value = True):
		dirX = 1 if x1 < x2 else -1
		dirY = 1 if y1 < y2 else -1
		for y in range(y1, y2+dirY, dirY):
			# print("y" , y)
			for x in range(x1, x2+dirX, dirX):
				# self.output()
				self.set(x, y, value)
				# print("x",x)
				# self.output()

	def output(self, padded = False, inverse = False):
		T = "██" if not inverse else "  "
		F = "  " if not inverse else "██"
		empty = ".."
		if padded:
			for row in self.padded:
			# print(row)
				print("".join([empty if i is None else T if not i else F for i in row]))
		else:
			for row in self.grid:
			# print(row)
				print("".join([empty if i is None else T if not i else F for i in row]))

	def addPatterns(self, version):

		# patterns = {1: [], 2: [6, 18], 3: [6,22], 4: [6,26], 5: [6,30],6:[6,34]}
		



		# top left finder
		self.fillArea(0, 0, 8, 8, False)
		self.fillArea(0, 0, 6, 6)
		self.fillArea(1, 1, 5, 5, False)
		self.fillArea(2, 2, 4, 4)
		# top right finder
		self.fillArea(self.size-8, 0, self.size-1, 8, False)
		self.fillArea(self.size-7, 0, self.size-1, 6)
		self.fillArea(self.size-6, 1, self.size-2, 5, False)
		self.fillArea(self.size-5, 2, self.size-3, 4)
		# bottom left finder
		self.fillArea(0, self.size-8, 8, self.size-1, False)
		self.fillArea(0, self.size-7, 6, self.size-1)
		self.fillArea(1, self.size-6, 5, self.size-2, False)
		self.fillArea(2, self.size-5, 4, self.size-3)

		# alignment
		if len(self.patternData[version]) > 0:
			patterns = [[x,y] for x in self.patternData[version] for y in self.patternData[version]]
			for p in patterns:
				if self.grid[p[1]][p[0]] is None:
					self.fillArea(p[0]-2,p[1]-2,p[0]+2,p[1]+2) 
					self.fillArea(p[0]-1,p[1]-1,p[0]+1,p[1]+1, False) 
					self.set(p[0],p[1])


		# spacing
		self.fillArea(6,8,6,self.size-8, False)
		self.fillArea(8,6,self.size-8,6, False)
		for i in range(8, self.size-8, 2):
			self.set(i, 6)
			self.set(6, i)

		# dark spot
		self.set(8, self.size-8)

		# print(self.grid)
		# input()
		self.validMap = [[(x == None) for x in row] for row in self.grid]
		# print(self.validMap)
		# input()

	def validSpace(self, x, y):
		return self.validMap[y][x]
		# if (x <= 8):
		# 	if (y <= 8 or y >= self.size - 8):
		# 		return False
		# if (x >= self.size - 8 and y <= 8):
		# 	return False
		# if (y == 6 or x == 6):
		# 	return False
		# return True



	
	def fillData(self, data, version):
		data += "0"*self.remainderBits[version]
		x = self.size - 1
		y = self.size - 1
		dirY = -1
		left = False
		charIndex = 0
		while charIndex < len(data):
			# self.output()
			# input()
			# if x <= 12:
			# 	input()
			# 	self.output()
			# print("left", left)
			# print(x - left, y)
			if self.validSpace(x - left, y):
				# print("valid")
				self.set(x - left, y, data[charIndex] == "1")
				# print(charIndex + 1, "/", len(data))
				charIndex += 1
			if left:
				left = False
				y += dirY
				if y == -1:
					y = 0
					dirY = 1
					x -= 2
					if x == 6:
						x = 5
				elif y == self.size:
					y = self.size - 1
					dirY = -1
					x -= 2
			else:
				left = True
			# self.output()
			# input()

	def mask1(self, x, y):
		if y % 2 == 0:
			return True
		return False

	def mask2(self, x, y):
		if x % 3 == 0:
			return True
		return False



	def applyMask(self, mask = 2):
		for x in range(self.size):
			for y in range(self.size):
				if self.validSpace(x, y):
					if mask == 1:
						self.grid[y][x] ^= self.mask1(x,y)
					if mask == 2:
						self.grid[y][x] ^= self.mask2(x, y)

	


	formatInfo = {"L":"01","M":"00","Q":"11","H":"10"}
	def addInfo(self, ec, mask):
		formatStr = self.formatInfo[ec] + intToBin(mask, 3) # correction Q, mask pattern 2
		# print(formatStr)

		# formatStr = "01100"
		xor = formatStr
		gen = "10100110111"

		xor += "0" * 10
		xor = xor.lstrip("0")
		# print(xor)
		# genPadded = gen.ljust(len(xor),"0")

		while len(xor) > 10:
			genPadded = gen.ljust(len(xor),"0")

			xor = stringXor(xor, genPadded)
			xor = xor.lstrip("0")
		# print(f"xor {xor}")
		if len(xor) < 10:
			xor = xor.rjust(10, "0")
		# print(f"xor padded {xor}")
		formatStr += xor
		# print(formatStr)
		formatStr = stringXor(formatStr, "101010000010010")
		# print(formatStr)
		# formatStr = "111111111111111"

		for i in range(6):
			self.set(i, 8, formatStr[i] == "1")
			self.set(8, self.size - i - 1, formatStr[i] == "1")
		self.set(8, self.size - 7, formatStr[6] == "1")
		self.set(7, 8, formatStr[6] == "1")
		self.set(8, 8, formatStr[7] == "1")
		self.set(8, 7, formatStr[8] == "1")
		self.set(self.size - 8, 8, formatStr[7] == "1")
		self.set(self.size - 7, 8, formatStr[8] == "1")
		for i in range(6):
			self.set(8, 5 - i, formatStr[9 + i] == "1")
			self.set(self.size - 6 + i, 8, formatStr[9 + i] == "1")

	def pad(self, size = 4):
		self.padded = [[False for h in range(self.size + size*2)] for i in range(self.size + size*2)]
		for y in range(self.size):
			for x in range(self.size):
				self.padded[y+size][x+size] = self.grid[y][x]


def stringXor(a, b):
	out = ""
	if (len(a) != len(b)):
		raise Exception(f"string Xor different lengths {a}   {b}")
	for i in range(len(a)):
		if b[i] == "1":
			if a[i] == "1":
				out += "0"
			else:
				out += "1"
		else:
			out += a[i]
	return out


# dataString = "badapple"
# encoded = encode(dataString)
# fromPower, asPower = calcGalois()


# poly = incPower(dataToPoly(encoded),13)     # coefficients are normal numbers
# codeWord = incPower(genCodeword(13),12)       # coefficients are powers

# print(fromPower)
# # print(asPower)

# print("generator (powers):")
# print(codeWord)
# print("encoded")
# print(encoded)
# print("message (ints):")
# print(poly)
# print(powerToCoeff(poly))
# correction = polyDivide(poly, codeWord)
# print(correction)
# finalBits = "".join([intToBin(i) for i in poly.values()] + [intToBin(i) for i in correction.values()])
# print(finalBits)

# st = finalBits[:12]
# for i in range(len(finalBits[12:])):
# 	if i%8 == 0:
# 		st += " "
# 	st += finalBits[12:][i]
# print(st)




# g = Grid(21)
# g.addPatterns()
# g.fillData(finalBits)

# g.applyMask()
# g.output()
# g.addInfo()
# g.output()
# g.pad(2)
# g.output(padded = True)


versionData = {1:{"L":{"dataLength":19,"ecPerBlock":7,"groups":[{"blockNum":1,"dataNum":19}]},"M":{"dataLength":16,"ecPerBlock":10,"groups":[{"blockNum":1,"dataNum":16}]},"Q":{"dataLength":13,"ecPerBlock":13,"groups":[{"blockNum":1,"dataNum":13}]},"H":{"dataLength":9,"ecPerBlock":17,"groups":[{"blockNum":1,"dataNum":9}]}},
2:{"L":{"dataLength":34,"ecPerBlock":10,"groups":[{"blockNum":1,"dataNum":34}]},"M":{"dataLength":28,"ecPerBlock":16,"groups":[{"blockNum":1,"dataNum":28}]},"Q":{"dataLength":22,"ecPerBlock":22,"groups":[{"blockNum":1,"dataNum":22}]},"H":{"dataLength":16,"ecPerBlock":28,"groups":[{"blockNum":1,"dataNum":16}]}},
3:{"L":{"dataLength":55,"ecPerBlock":15,"groups":[{"blockNum":1,"dataNum":55}]},"M":{"dataLength":44,"ecPerBlock":26,"groups":[{"blockNum":1,"dataNum":44}]},"Q":{"dataLength":34,"ecPerBlock":18,"groups":[{"blockNum":2,"dataNum":17}]},"H":{"dataLength":26,"ecPerBlock":22,"groups":[{"blockNum":2,"dataNum":13}]}},
4:{"L":{"dataLength":80,"ecPerBlock":20,"groups":[{"blockNum":1,"dataNum":80}]},"M":{"dataLength":64,"ecPerBlock":18,"groups":[{"blockNum":2,"dataNum":32}]},"Q":{"dataLength":48,"ecPerBlock":26,"groups":[{"blockNum":2,"dataNum":24}]},"H":{"dataLength":36,"ecPerBlock":16,"groups":[{"blockNum":4,"dataNum":9}]}},
5:{"L":{"dataLength":108,"ecPerBlock":26,"groups":[{"blockNum":1,"dataNum":108}]},"M":{"dataLength":86,"ecPerBlock":24,"groups":[{"blockNum":2,"dataNum":43}]},"Q":{"dataLength":62,"ecPerBlock":18,"groups":[{"blockNum":2,"dataNum":15},{"blockNum":2,"dataNum":16}]},"H":{"dataLength":46,"ecPerBlock":22,"groups":[{"blockNum":2,"dataNum":11},{"blockNum":2,"dataNum":12}]}}}

fromPower, asPower = calcGalois()
def genCorr(bits, length):
	poly = incPower(dataToPoly(bits),length)     # coefficients are normal numbers
	codeWord = incPower(genCodeword(length),max(poly.keys()) - length)       # coefficients are powers
	correction = polyDivide(poly, codeWord)
	# print(correction)
	return "".join([intToBin(i) for i in correction.values()])
	# return correction


# example = [intToBin(int(i)) for i in "64, 71, 70, 87, 55, 64, 236, 17, 236, 17, 236, 17, 236, 17, 236".split(", ")]
# print("".join(example))
# print([int(i,2) for i in example])
# print(genCorr("".join(example), 18))
# input()


def gen(text, version = 1, correction = "Q"):
	global fromPower, asPower
	# corrWordNums = {"1-Q":13}
	# wordNum = str(version)+"-"+correction
	# if not wordNum in corrWordNums:
	# 	print("version unavailable")
	# 	return

	# errNum = corrWordNums[wordNum]

	qrData = versionData[version][correction]

	gridSize = ((version-1)*4)+21


	encoded = encode(text, qrData["dataLength"])
	# print(encoded)

	blocks = []
	offset = 0

	for group in qrData["groups"]:
		# print("group",group)
		for block in range(group["blockNum"]):
			# print("block",block)
			blocks.append(encoded[offset:offset+group["dataNum"]*8])
			offset += group["dataNum"]*8

	# print(blocks)

	ecs = []
	ecPerBlock = qrData["ecPerBlock"]
	offset = 0
	blockIndex = 0
	for i in blocks:
		ecs.append(genCorr(i, ecPerBlock))

	
	blocks = [[i[x*8:x*8+8] for x in range(len(i)//8)] for i in blocks]
	ecs = [[i[x*8:x*8+8] for x in range(len(i)//8)] for i in ecs]

	# print(blocks)

	finalBytes = []
	for i in range(max([len(x) for x in blocks])):
		for blockNum in range(len(blocks)):
			if len(blocks[blockNum]) > 0:
				finalBytes.append(blocks[blockNum].pop(0))

	for i in range(max([len(x) for x in ecs])):
		for blockNum in range(len(ecs)):
			if len(ecs[blockNum]) > 0:
				finalBytes.append(ecs[blockNum].pop(0))

	# print(finalBytes)




	# input()





	
	
	# poly = incPower(dataToPoly(encoded),errNum)     # coefficients are normal numbers
	# codeWord = incPower(genCodeword(errNum),max(poly.keys()) - errNum)       # coefficients are powers
	# # print(poly)
	# # print(codeWord)
	# correction = polyDivide(poly, codeWord)
	# finalBits = "".join([intToBin(i) for i in poly.values()] + [intToBin(i) for i in correction.values()])

	g = Grid(gridSize)
	# print(g.grid)
	# g.output()
	g.addPatterns(version)
	# print(g.grid)
	# g.output()
	# input()
	g.fillData("".join(finalBytes), version)
	# g.output()

	g.applyMask(1)
	# print(finalBits)
	# g.output()
	g.addInfo(correction, 1)

	return g
	# g.output()
	# g.pad(2)
	# g.output(padded = True)


# qr = gen("hello")
# qr.pad(2)
# qr.output(True)

# g = gen("test",5,"Q")
# g.pad(2)
# g.output(padded = True)