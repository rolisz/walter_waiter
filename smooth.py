import math

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def getPositions(fromPos, toPos, steps):
    imageLen = (sigmoid(5) - sigmoid(-5))
    ratio = (toPos - fromPos) / imageLen
    offset = fromPos
    positions = []
    x = -4
    while x<=4:
        positions.append(offset+ratio*sigmoid(x))
        x+= 8.0 / (steps-1)
    return positions

def getSpeeds(distance, steps):
    fromPos = 0
    toPos = distance
    positions = getPositions(fromPos, toPos, steps)
    speeds = []
    speeds.append(0)
    for i in range(len(positions)-1):
        speeds.append(positions[i+1]-positions[i])
    speeds.append(0)
    return speeds

if __name__=='__main__':
    for x in getSpeeds(100, 20):
        print x

