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
    for i in reversed(list(range(len(connects)))):  # TODO still sth wrong if not fixed
        if i == 0:
            break
        break_ = False
        for pos in connects[i]:
            for j in range(i):
                for pos2 in connects[j]:
                    if pos2[0] == pos[0] - 1:
                        connects[j] = connects[j] | connects[i]
                        connects.pop(i)
                        break_ = True
                        break
                if break_:
                    break
            if break_:
                break

    return connects


def connection2(inpl, valid):
    valids = set()
    connections = []

    def dps(x, y):
        connect = set()
        connect.add((x, y))
        valids.add((x, y))
        if x + 1 < len(inpl):
            if valid(inpl[x + 1][y]) and (x + 1, y) not in valids:
                new = dps(x + 1, y)
                connect = new | connect
        if x - 1 > -1:
            if valid(inpl[x - 1][y]) and (x - 1, y) not in valids:
                new = dps(x - 1, y)
                connect = new | connect
        if y + 1 < len(inpl[0]):
            if valid(inpl[x][y + 1]) and (x, y + 1) not in valids:
                new = dps(x, y + 1)
                connect = new | connect
        if y - 1 > -1:
            if valid(inpl[x][y - 1]) and (x, y - 1) not in valids:
                new = dps(x, y - 1)
                connect = new | connect
        return connect

    for i, line in enumerate(inpl):
        for j, item in enumerate(line):
            if valid(item) and (i, j) not in valids:
                # print(f"call dps at {i}, {j}")
                new_connect = dps(i, j)
                connections.append(new_connect)
                pass

    # print(f"valids: {valids}")
    return connections


def main():
    print(connection(np.array([[1, 1, 0, 0],
                               [1, 1, 0, 0],
                               [1, 0, 0, 1],
                               [0, 0, 0, 1]]), lambda x: x == 1))


if __name__ == "__main__":
    main()
