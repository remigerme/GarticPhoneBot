from pyautogui import locateOnScreen, locateCenterOnScreen, screenshot


def locate_playground():
    try:
        (x, y, w, h) = locateOnScreen("pictures/playground_block.png")
    except TypeError:
        raise Exception("Unable to locate playground")
    screen = screenshot()
    while screen.getpixel((x + w, y + h)) == (255, 255, 255):
        w += 1
    while screen.getpixel((x + w - 1, y + h)) == (255, 255, 255):
        h += 1
    return (x, y, w - 1, h - 1)

def locate_palette(colors):
    p_locations = {}
    for (r, g, b) in colors:
        try:
            (x, y) = locateCenterOnScreen("pictures/p_{}_{}_{}.png".format(r, g, b))
            p_locations[(r, g, b)] = (x, y)
        except TypeError:
            raise Exception("Unable to locate ({}, {}, {})".format(r, g, b))
    
    return p_locations
