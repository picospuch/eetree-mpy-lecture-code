### fft.py --- fft by cooley-tukey algorithm

## author: picospuch

## ref: https://create.arduino.cc/projecthub/abhilashpatel121/easyfft-fast-fourier-transform-fft-for-arduino-9d2677

### Code:

from math import sqrt

sine_data = b'\x00\x04\t\r\x12\x16\x1b\x1f#(,159>BFKOSW[`dhlptx|\x7f\x83\x87\x8b\x8f\x92\x96\x99\x9d\xa0\xa4\xa7\xab\xae\xb1\xb4\xb7\xba\xbd\xc0\xc3\xc6\xc9\xcc\xce\xd1\xd3\xd6\xd8\xdb\xdd\xdf\xe1\xe3\xe5\xe7\xe9\xeb\xec\xee\xf0\xf1\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfd\xfe\xfe\xfe\xff\xff\xff\xff'
def sine(i):
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
    return out/255

def cosine(i):
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

f_peaks = [0 for _ in range(5)]
f_peaks_amp = [0 for _ in range(5)]

def fft(time_series, n_time_series, freq):
    """ calculate fft of 'time_series
    time_series - time series input data array
    n_time_series - size of 'time_series
    freq - sampling frequency
    """
    size_array = [1,2,4,8,16,32,64,128,256,512,1024,2048] # size-array of time_series, level is its index
    
    # 0. calculating the levels
    # l - the level
    for i in range(12):
        if size_array[i] <= n_time_series:
            l = i
    
    in_ps = [0 for _ in range(size_array[l])] # position array
    out_real = [0 for _ in range(size_array[l])] # output real part array
    out_imaginary = [0 for _ in range(size_array[l])] # output imaginary part array
    
    # 1. bit-reverssing - get new position array
    x = 0
    for i in range(l):
        n = size_array[i] # size at level i
        n_div = int(size_array[l]/(n + n))
        
        for j in range(n):
            x = x + 1
            in_ps[x] = in_ps[j] + n_div
            
    # 2. time-series-sorting by bit reversed order
    for i in range(size_array[l]):
        if in_ps[i] < n_time_series:
            out_real[i] = time_series[in_ps[i]]
        if in_ps[i] > n_time_series:
            out_real[i] = time_series[in_ps[i] - n_time_series]

    # 3. fft
    for i in range(l):
        n = size_array[i]
        n_s = int(size_array[l] / size_array[i + 1]) # n, similar
        
        e = 360 / size_array[i + 1]
        e = 0 - e
        n1 = 0
        
        for j in range(n):
            c = cosine(int(e * j))
            s = sine(int(e * j))
            n1 = j
            
            for k in range(n_s):
                tr = c * out_real[n + n1] - s * out_imaginary[n + n1]
                ti = s * out_real[n + n1] + c * out_imaginary[n + n1]
                
                out_real[n1 + n] = out_real[n1] - tr
                out_real[n1] = out_real[n1] + tr
                
                out_imaginary[n1 + n] = out_imaginary[n1] - ti
                out_imaginary[n1] = out_imaginary[n1] + ti
                
                n1 = n1 + n + n
    
    # print vector
    # for i in range(size_array[l]):
    #     print(str(i) + "\t" + str(out_real[i]) + "\t" + str(out_imaginary[i]) + "i")
    
    # 4. vector-modulus-caculating
    for i in range(size_array[l]):
        out_real[i] = sqrt(out_real[i] * out_real[i] + out_imaginary[i] * out_imaginary[i])
        out_imaginary[i] = i * freq / n_time_series
    
    # print (amp, freq)
    # for i in range(size_array[l]):
    #     print("({0}, {1})".format(out_real[i], out_imaginary[i]))

    # 5. peak-detection
    x = 0
    for i in range(size_array[l] - 1):
        if out_real[i] > out_real[i-1] and out_real[i] > out_real[i+1]:
            in_ps[x] = i;
            x = x + 1
    
    # 6. sort-by-amplitude
    s = 0
    c = 0
    for i in range(x):
        for j in range(c, x):
            if out_real[in_ps[i]] < out_real[in_ps[j]]:
                s = in_ps[i]
                in_ps[i] = in_ps[j]
                in_ps[j] = s
        c = c + 1
    
    for i in range(5):
        f_peaks[i] = out_imaginary[in_ps[i]]
        f_peaks_amp[i] = out_real[in_ps[i]]
