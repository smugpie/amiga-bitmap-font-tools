const convertToColor = (colorWord) => {
    const red = Math.floor(colorWord / 256);
    const byte2 = colorWord % 256;
    const green = Math.floor(byte2 / 16);
    const blue = byte2 % 16;

    return {
        raw: {
            red,
            green,
            blue
        },
        red: convert4BitToBitComponent(red),
        green: convert4BitToBitComponent(green),
        blue: convert4BitToBitComponent(blue),
        hex: convertToHex(red, green, blue)
    }
}

const convert4BitToBitComponent = (component) => {
    return component * 17;    
}

const convertToHex = (red, green, blue) => {
    const r = convert4BitToBitComponent(red);
    const g = convert4BitToBitComponent(green);
    const b = convert4BitToBitComponent(blue);

    const decimalColor = r * 65536 + g * 256 + b;
    return ("000000" + decimalColor.toString(16)).slice(-6);
}

module.exports = { convertToColor }
