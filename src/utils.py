from time import sleep
from platform import system

SYS = system().lower()
if SYS == "windows" or SYS == "linux":
    import mouse
else: # macos ie sys = "darwin"
    pass


def click(x, y):
    mouse.move(x, y, True, 0)
    sleep(1e-6)
    mouse.click("left")
