def bitIsSet( value, bit ):
    bitSet = value & (2 ** bit)
    print('value', value, 'bit', bit, value & (2 **  bit))
    return True if bitSet > 0 else False

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getRange(lst, start, length):
    return lst[start:start + length]
