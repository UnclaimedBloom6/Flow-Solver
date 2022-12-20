from PIL import Image

def mono(image: Image.Image, threshold=60):
    fn = lambda x : 255 if x < threshold else 0
    return image.point(fn, mode='1')

# https://www.lihaoyi.com/post/Ansi/RainbowBackground256.png

colors = {
    "Light Blue": {
        "gray_value": 179,
        "ansi": "\u001b[48;5;51m"
    },
    "Yellow": {
        "gray_value": 211,
        "ansi": "\u001b[48;5;226m"
    },
    "Red": {
        "gray_value": 76,
        "ansi": "\u001b[48;5;1m"
    },
    "Purple": {
        "gray_value": 53,
        "ansi": "\u001b[48;5;90m"
    },
    "Pink": {
        "gray_value": 105,
        "ansi": "\u001b[48;5;13m"
    },
    "Blue": {
        "gray_value": 29,
        "ansi": "\u001b[48;5;4m"
    },
    "Green": {
        "gray_value": 75,
        "ansi": "\u001b[48;5;2m"
    },
    "Orange": {
        "gray_value": 151,
        "ansi": "\u001b[48;5;172m"
    },
    "Dark Red": {
        "gray_value": 79,
        "ansi": "\u001b[48;5;88m"
    },
    "Lime": {
        "gray_value": 150,
        "ansi": "\u001b[48;5;10m"
    },
    "White": {
        "gray_value": 255,
        "ansi": "\u001b[48;5;15m"
    },
    "Gray": {
        "gray_value": 128,
        "ansi": "\u001b[48;5;240m"
    },
    "Olive": {
        "gray_value": 176,
        "ansi": "\u001b[48;5;100m"
    },
    "Cyan": {
        "gray_value": 90,
        "ansi": "\u001b[48;5;30m"
    },
    "Dark Blue": {
        "gray_value": 16,
        "ansi": "\u001b[48;5;17m"
    }
}

ANSI_RESET = "\u001b[0m"

def print_square(color: str, text=False, amount=1, new_line=False):
    output = ""
    if color in colors:
        output = colors[color]["ansi"]
    output += " "
    if text and color is not None:
        output += color[0]
        output += " "
    else:
        output += "  "
    
    output += ANSI_RESET
    output *= amount

    if new_line:
        print(output)
    else:
        print(output, end="")