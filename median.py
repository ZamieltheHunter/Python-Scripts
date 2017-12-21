from math import floor
def median(sequence):
    temp = sorted(sequence)
    print(sorted(sequence))
    print(len(temp))
    if(len(temp) % 2 != 0):
        return temp[int(floor(len(temp)/2))]
    else:
        print(len(temp)/2)
        return ((temp[int(len(temp)/2)] + temp[int(len(temp)/2) - 1]) / 2.0)

print(median([4,5,5,4]))
