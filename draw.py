import gen
import pygame

# pygame.init()

target = "3<           "
version = 1
corLvl = "Q"
gridSize = ((version-1)*4)+21

g = gen.gen(target, version, corLvl)
# g.output()
# print(gen.decode("10111101111111111111"))
# input()"00000000000"+"00000000000"+"0"*12+"0"*12
# target = "00000000000"+"00000000000"+"0"*12+"0"*12
# g2 = gen.gen(target, version, corLvl)

# g3 = gen.Grid(gridSize)
# g3.grid = [[g.grid[y][x]==g2.grid[y][x] for x in range(len(g.grid))] for y in range(len(g.grid))]
# g3.output()
# input()





# print(g.grid)


def renderGrid(grid, pixelSize):
	for y in range(g.size):
		for x in range(g.size):
			pygame.draw.rect(screen, ((not g.grid[y][x])*255,(not g.grid[y][x])*255,(not g.grid[y][x])*255), pygame.Rect(x*pixelSize,y*pixelSize,pixelSize,pixelSize))



totalSize = (26)*8

regions = []
testGrid = gen.Grid(gridSize)
testGrid.addPatterns(version)
testGrid.fillData("0"*totalSize,version)
testGrid.applyMask(1)
testGrid.output()
# input()
for i in range((totalSize) // 8):
	toTest = "0"*8*i + "1"*8 + "0"*(totalSize - 8*(i+1))
	# print(toTest)
	
	testGrid.fillData(toTest, version)
	# regions.append(g.grid)
	current = []
	for y in range(gridSize):
		for x in range(gridSize):
			# print(g.grid[y][x])
			# input()
			if testGrid.grid[y][x]:
				current.append((x,y))
	# testGrid.output()
	# print(toTest)
	# input()
	regions.append(current)


def drawRegions(pixelSize):
	regionsSurface.fill((0,0,0,0))
	for n, i in enumerate(regions):
		for square in i:
			pygame.draw.rect(regionsSurface, (n*123%255,n*456%255,n*67%255, 200), pygame.Rect(square[0]*pixelSize, square[1]*pixelSize,pixelSize,pixelSize))


flipped = []
corrupted = {i: 0 for i in range(len(regions))}
def click(x, y):
	if x >= gridSize or y >= gridSize:
		return
	if (x, y) in flipped:
		flipped.remove((x,y))
		for n,i in enumerate(regions):
			if (x,y) in i:
				corrupted[n] -= 1
				break
	else:
		flipped.append((x,y))
		for n,i in enumerate(regions):
			if (x,y) in i:
				corrupted[n] += 1
				break
	g.grid[y][x] = not g.grid[y][x]

	print(corrupted)


pixelSize = 10

screen = pygame.display.set_mode((gridSize*pixelSize+100,gridSize*pixelSize+50))
regionsSurface = pygame.Surface((gridSize*pixelSize,gridSize*pixelSize), pygame.SRCALPHA)

maxCorruptible = 6


running = True 
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			click(pos[0]//pixelSize, pos[1]//pixelSize)
			g.pad()
			g.output(padded=True)
			print(f"corrupted regions: {len([i for i in corrupted if corrupted[i] > 0])}/{maxCorruptible}")
			
	screen.fill((255,255,255))
	renderGrid(g, pixelSize)
	drawRegions(pixelSize)
	screen.blit(regionsSurface, (0,0))
	pygame.display.flip()
	# renderGrid()

# Quit Pygame
pygame.quit()