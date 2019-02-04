import numpy as np


def connection(inpl, valid):
    connects = []

    # detect connects horizontally
    for line_num, line in enumerate(inpl):
        for item_num, item in enumerate(line):
            if valid(item):
                if connects:
                    if item_num > 0 and (line_num, item_num - 1) in connects[-1]:
                        connects[-1].add((line_num, item_num))
                    else:
                        connects.append(set([(line_num, item_num)]))
                else:
                    connects.append(set([(line_num, item_num)]))

    # detects connects vertically
    for i, connect in list(enumerate(connects))[::-1]:
        if i == 0:
            break
        for line_num, item_num in connect:
            for i2, j in enumerate(connects):
                if i2 != i and (line_num - 1, item_num) in j:
                    connects[i2] = connects[i2] | connect
                    try:
                        connects.pop(i)
                    except IndexError:
                        pass

    return connects


def main():
    print(connection(np.array([[1, 1, 0, 0],
                               [1, 1, 0, 0],
                               [1, 0, 0, 1],
                               [0, 0, 0, 1]]), lambda x: x == 1))


if __name__ == "__main__":
    main()
