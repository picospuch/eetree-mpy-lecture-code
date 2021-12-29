### p_math.py --- mathematics library of picospuch

## author: picospuch

### Code:

sine_data = b'\x00\x04\t\r\x12\x16\x1b\x1f#(,159>BFKOSW[`dhlptx|\x7f\x83\x87\x8b\x8f\x92\x96\x99\x9d\xa0\xa4\xa7\xab\xae\xb1\xb4\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xce\xd1\xd3\xd6\xd8\xdb\xdd\xdf\xe1\xe3\xe5\xe7\xe9\xeb\xec\xee\xf0\xf1\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfd\xfe\xfe\xfe\xff\xff\xff\xff'

pi = 3.141592653
def sin(i):
    j = i
    while j<0:
        j=j+360
    while j>360:
        j=j-360
    if j>-1 and j<91:
        out = sine_data[j]
    elif j>90 and j<181:
        out = sine_data[180-j]
    elif j>180 and j<271:
        out = -sine_data[j-180]
    elif j>270 and j<361:
        out = -sine_data[360-j]
    return (out/255)

def cos(i):
    j = i
    while j<0:
        j=j+360
    while j>360:
        j=j-360
    if j>-1 and j<91:
        out = sine_data[90-j]
    elif j>90 and j<181:
        out = -sine_data[j-90]
    elif j>180 and j<271:
        out = -sine_data[270-j]
    elif j>270 and j<361:
        out = sine_data[j-270]
    return (out/255)
