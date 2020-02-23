#!/usr/local/bin/python3
#
# Paul Evans (10evans@sandiego.edu)
# 21 February 2020
#
def main():
    token_frequencies = eval(open('./save.txt', 'r').read())
    # print(token_frequencies['zizania'])
    keys = list(token_frequencies.keys())
    values = list(token_frequencies.values())
    print(keys[0:150])
    print(values[0:150])
    sum = 0
    for i in range(500):
        sum += values[i]
        if sum > 212369: break
    print(i)

    

if __name__ == '__main__':
    main()
