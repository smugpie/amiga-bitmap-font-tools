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

const expandFlags = (flags) => ({
    value: flags,
    disk: bitIsSet(flags, 1),
    proportional: bitIsSet(flags, 5),
    designed: bitIsSet(flags, 6)
});

const expandColorFlags = (flags) => ({
    value: flags,
    colorFont: bitIsSet(flags, 0),
    grayFont: bitIsSet(flags, 1)
});

module.exports = {
    bitIsSet,
    expandStyle,
    expandFlags,
    expandColorFlags
}
