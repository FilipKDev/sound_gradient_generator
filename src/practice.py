# Contains functions written just for programming practice
# Will be replaced by NumPy functionality in the final version

import decimal

def NumArray1D(start, end, step, endpoint = True):
    s = decimal.Decimal(str(step))
    a = decimal.Decimal(str(start))
    b = decimal.Decimal(str(end))
    precision = -s.as_tuple().exponent
    decimal.getcontext().prec = precision + 2

    end_loop = (b - a) / s
    original_rounding = decimal.getcontext().rounding
    decimal.getcontext().rounding = decimal.ROUND_CEILING
    end_loop = int(round(end_loop, 0))

    array = []
    
    for i in range(end_loop):
        i *= s
        i += a
        array.append(float(i))

    decimal.getcontext().rounding = original_rounding

    last_item = decimal.Decimal(array[-1]) + s
    if endpoint and last_item == b:
        array.append(float(last_item))

    return array

def NumArray1D_Lin(start, end, num, endpoint = True):
    mult = (end - start) / num
    array = [i * mult + start for i in range(num)]
    if endpoint:
        array.append(end)
    return array

def NumArray2D_V(start, end, step, height, endpoint = True):
    line = NumArray1D(start, end, step, endpoint)
    array = []
    for i in range(height):
        array.append(line)
    return array

def NumArray2D_H(start, end, step, width, endpoint = True):
    col = NumArray1D(start, end, step, endpoint)
    array = []
    for i in range(len(col)):
        line = []
        for j in range(width):
            line.append(col[i])
        array.append(line)
    return array

def NumArray2D_VLin(start, end, num, height, endpoint = True):
    line = NumArray1D_Lin(start, end, num, endpoint)
    array = []
    for i in range(height):
        array.append(line)
    return array

def NumArray2D_HLin(start, end, num, width, endpoint = True):
    col = NumArray1D_Lin(start, end, num, endpoint)
    array = []
    for i in range(len(col)):
        line = []
        for j in range(width):
            line.append(col[i])
        array.append(line)
    return array