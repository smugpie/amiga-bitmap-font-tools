def convert4BitToBitComponent(component):
    return component * 17


def convertToHex(red, green, blue):
    r = convert4BitToBitComponent(red)
    g = convert4BitToBitComponent(green)
    b = convert4BitToBitComponent(blue)

    decimalColor = r * 65536 + g * 256 + b
    return f"{decimalColor:0>6x}"


def convertToColor(colorWord):
    red = int(colorWord / 256)
    byte2 = colorWord % 256
    green = int(byte2 / 16)
    blue = byte2 % 16

    return {
        "raw": {
            red,
            green,
            blue
        },
        "red": convert4BitToBitComponent(red),
        "green": convert4BitToBitComponent(green),
        "blue": convert4BitToBitComponent(blue),
        "hex": convertToHex(red, green, blue),
        "fontColor": [red / 15.0, green / 15.0, blue / 15.0, 1.0]
    }
