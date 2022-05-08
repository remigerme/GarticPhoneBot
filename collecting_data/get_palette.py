from pyautogui import pixel, position

def get_rgb():
    return pixel(*position())

def main ():
    s = []
    for i in range(18):
        input(i)
        s.append(get_rgb())

    with open("gp_palette.txt", "w") as f:
        for e in s:
            f.write(str(e) + "\n")

if __name__ == "__main__":
    main()
