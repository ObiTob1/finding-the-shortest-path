def buildTrajectory(start, cords):
    N = len(cords)
    stepsX = []
    stepsY = []
    for i in range(N - 1):
        prev = cords[i]
        finish, x, y = turn(start, prev, Ns=40)
        stepsX += x
        stepsY += y
        next = cords[i + 1]
        toNextCenter = {
            "x": next["x"] - finish["x"],
            "y": next["y"] - finish["y"]
        }
        sinAlpha = next["radius"] / math.sqrt(toNextCenter["x"]**2 + toNextCenter["y"]**2)
        alpha = math.asin(sinAlpha)
        tangentModule = math.sqrt(toNextCenter["x"]**2 + toNextCenter["y"]**2) * math.cos(alpha)
        
        prevSide = prev["side"]
        nextSide = next["side"]
        if nextSide == "RIGHT":
            alpha = -alpha
        
        
        turnedX_new = toNextCenter["x"] * math.cos(alpha) - toNextCenter["y"] * math.sin(alpha)
        turnedY_new = toNextCenter["x"] * math.sin(alpha) + toNextCenter["y"] * math.cos(alpha)

        turnedModule = math.sqrt(turnedX_new**2 + turnedY_new**2)

        strightFinish = {
            "x": finish["x"] + turnedX_new * tangentModule / turnedModule,
            "y": finish["y"] + turnedY_new * tangentModule / turnedModule,
        }

        start, x, y = stright(finish, strightFinish, 10)
        stepsX += x
        stepsY += y
    return stepsX, stepsY

def turn(start, point, Ns=10):
    stepsX = []
    stepsY = []

    radius = {
        "x": start["x"] - point["x"],
        "y": start["y"] - point["y"]
    }
    phi = point["turn"] / Ns * math.pi / 180
    for step in range(Ns):
        x_new = point["x"] + radius["x"]*math.cos(phi) - radius["y"] * math.sin(phi)
        y_new = point["y"] + radius["x"]*math.sin(phi) + radius["y"] * math.cos(phi)
        radius["x"] = x_new - point["x"]
        radius["y"] = y_new - point["y"]
        stepsX.append(point["x"] + radius["x"])
        stepsY.append(point["y"] + radius["y"])

    finish = {
        "x": x_new,
        "y": y_new
    }
    return finish, stepsX, stepsY


def stright(start, end, steps=5):
    stepsX = []
    stepsY = []
    module = math.sqrt((end["x"] - start["x"])**2 + (end["y"] - start["y"])**2)
    stepSize = module / steps
    l = {
        "x": (end["x"] - start["x"]) * stepSize / module,
        "y": (end["y"] - start["y"]) * stepSize / module
    }
    for step in range(steps):
        stepsX.append(start["x"] + l["x"])
        stepsY.append(start["y"] + l["y"])
        start["x"] = start["x"] + l["x"]
        start["y"] = start["y"] + l["y"]
    return start, stepsX, stepsY