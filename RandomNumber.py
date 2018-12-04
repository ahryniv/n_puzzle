import time


def random_number_below(n):
    n2 = int(time.time() * 1000000)
    return n2 % n


if __name__ == "__main__":
    results = {}
    for i in range(1000):
        r_n = random_number_below(4)
        if r_n in results:
            results[r_n] += 1
        else:
            results[r_n] = 1
    print(results)
