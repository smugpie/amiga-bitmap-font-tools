def bitIsSet( value, bit ):
    bitSet = value & (2 ** bit)
    return True if bitSet > 0 else False


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def getRange(lst, start, length):
    return lst[start:start + length]


def getNiceGlyphName(unicode):
    glyphNames = [
        'space', 'exclam', 'quotedbl', 'numbersign', 'dollar', 'percent', 'ampersand',
        'quotesingle', 'parenleft', 'parenright', 'asterisk', 'plus', 'comma', 'hyphen',
        'period', 'slash', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine', 'colon', 'semicolon', 'less', 'equal', 'greater', 'question',
        'at', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'bracketleft', 'backslash',
        'bracketright', 'asciicircum', 'underscore', 'grave', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'braceleft', 'bar', 'braceright', 'asciitilde', 'DEL', 'uni0080',
        'uni0081', 'uni0082', 'uni0083', 'uni0084', 'uni0085', 'uni0086', 'uni0087',
        'uni0088', 'uni0089', 'uni008a', 'uni008b', 'uni008c', 'uni008d', 'uni008e',
        'uni008f', 'uni0090', 'uni0091', 'uni0092', 'uni0093', 'uni0094', 'uni0095',
        'uni0096', 'uni0097', 'uni0098', 'uni0099', 'uni009a', 'uni009b', 'uni009c',
        'uni009d', 'uni009e', 'uni009f', 'nbspace', 'exclamdown', 'cent',  'sterling',
        'currency', 'yen', 'brokenbar', 'section', 'dieresis', 'copyright', 'ordfeminine',
        'guillemotleft', 'logicalnot', 'softhyphen', 'registered', 'macron', 'degree',
        'plusminus', 'twosuperior', 'threesuperior', 'acute', 'micro', 'paragraph',
        'periodcentered', 'cedilla', 'onesuperior', 'ordmasculine', 'guillemotright',
        'onequarter', 'onehalf', 'threequarters', 'questiondown', 'Agrave', 'Aacute',
        'Acircumflex', 'Atilde', 'Adieresis', 'Aring', 'AE', 'Ccedilla', 'Egrave',
        'Eacute', 'Ecircumflex', 'Edieresis', 'Igrave', 'Iacute', 'Icircumflex', 'Idieresis',
        'Eth', 'Ntilde', 'Ograve', 'Oacute', 'Ocircumflex', 'Otilde', 'Odieresis',
        'multiply', 'Oslash', 'Ugrave', 'Uacute', 'Ucircumflex', 'Udieresis', 'Yacute',
        'Thorn', 'germandbls', 'agrave', 'aacute', 'acircumflex', 'atilde', 'adieresis',
        'aring', 'ae', 'ccedilla', 'egrave', 'eacute', 'ecircumflex', 'edieresis', 'igrave',
        'iacute', 'icircumflex', 'idieresis', 'eth', 'ntilde', 'ograve', 'oacute',
        'ocircumflex', 'otilde', 'odieresis', 'divide', 'oslash', 'ugrave', 'uacute',
        'ucircumflex', 'udieresis', 'yacute', 'thorn', 'ydieresis'
    ]
    return glyphNames[unicode - 32]


def getCodeMap(codepage):
    codeMaps = {
        'AmigaPL': {
            0xC2: (0x0104, 'Aogonek'),
            0xCA: (0x0106, 'Cacute'),
            0xCB: (0x0118, 'Eogonek'),
            0xCE: (0x0141, 'Lslash'),
            0xCF: (0x0143, 'Nacute'),
            0xD3: (0x00D3, 'Oacute'),
            0xD4: (0x015A, 'Sacute'),
            0xDA: (0x0179, 'Zacute'),
            0xDB: (0x017B, 'Zdotaccent'),
            0xE2: (0x0105, 'aogonek'),
            0xEA: (0x0107, 'cacute'),
            0xEB: (0x0119, 'eogonek'),
            0xEE: (0x0142, 'lslash'),
            0xEF: (0x0144, 'nacute'),
            0xF3: (0x00F3, 'oacute'),
            0xF4: (0x015B, 'sacute'),
            0xFA: (0x017A, 'zacute'),
            0xFB: (0x017C, 'zdotaccent'),
        }
    }
    if codepage in ('AmigaPL', 'amigapl', 'amiga-pl'):
        return codeMaps['AmigaPL']
    return None
