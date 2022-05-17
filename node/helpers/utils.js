const bitIsSet = (value, bit) => !!(value & (2 ** bit));

const expandStyle = (style) => ({
    value: style,
    normal: style === 0,
    underlined: bitIsSet(style, 0),
    bold: bitIsSet(style, 1),
    italic: bitIsSet(style, 2),
    extended: bitIsSet(style, 3),
    colorFont: bitIsSet(style, 6),
    tagged: bitIsSet(style, 7)
});

const expandFlags = (flags, fullContents = false) => {
    let expandedFlags = {
        value: flags,
        disk: bitIsSet(flags, 1),
        proportional: bitIsSet(flags, 5),
        designed: bitIsSet(flags, 6)
    };

    if (fullContents) {
        expandedFlags = {
            ...expandedFlags,
            rom: bitIsSet(flags, 0),
            reversed: bitIsSet(flags, 2),
            tallDot: bitIsSet(flags, 3),
            wideDot: bitIsSet(flags, 4),
            removed: bitIsSet(flags, 7)
        }
    }
    return expandedFlags;
};

const expandColorFlags = (flags) => ({
    value: flags,
    colorFont: bitIsSet(flags, 0),
    grayFont: bitIsSet(flags, 1)
});

const getFileContentsType = (fontFile) => {
    const fileContentsType = fontFile.readUInt16BE(0);
    const fileContentsFormats = {
        0xF00: 'FontContents',
        0xF02: 'TFontContents',
        0xF03: 'Scalable'
    }

    return fileContentsFormats[fileContentsType] || 'Unknown';
}

module.exports = {
    bitIsSet,
    expandStyle,
    expandFlags,
    expandColorFlags,
    getFileContentsType
}
