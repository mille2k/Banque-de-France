import sys
import mmap
import math
from time import sleep
from multiprocessing import Manager, Pool


### TRACKING:

def flipper(nmax, q):
    with open('atkin.data', 'w+b') as f:
        for _ in range(nmax // 8 + 1):
            f.write(b'\0')
        f.flush()
        with mmap.mmap(f.fileno(), 0) as mm:
            while True:
                t = q.get()
                if t is None:
                    return
                n, op = t
                if op == 'flip':
                    mm[n//8] ^= (1 << (n % 8))
                elif op == 'reset':
                    mm[n//8] &= ~(1 << (n % 8))


def check_table():
    with open('atkin.data', 'r+b') as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            for byte in mm:
                for i in range(8):
                    yield ord(byte) & 1 << i


def watcher(progressq):
    progress_all = {}
    while True:
        sleep(10)
        while not progressq.empty():
            process, progress = progressq.get()
            progress_all[process] = progress
        print(', '.join('{0}: {1:.2f}%'.format(k, v * 100)
                        for k, v in progress_all.items()))


### COMPUTING:

def atkin1(nmax, q, progressq):
    xymax = int(math.sqrt(nmax)) + 1
    for x in range(1, xymax):
        for y in range(1, xymax):
            n = 4*x**2 + y**2
            if (n <= nmax) and ((n % 12 == 1) or (n % 12 == 5)):
                q.put((n, 'flip'))
        progressq.put(('process1', x / (xymax - 1)))


def atkin2(nmax, q, progressq):
    xymax = int(math.sqrt(nmax)) + 1
    for x in range(1, xymax):
        for y in range(1, xymax):
            n = 3*x**2 + y**2
            if (n <= nmax) and (n % 12 == 7):
                q.put((n, 'flip'))
        progressq.put(('process2', x / (xymax - 1)))


def atkin3(nmax, q, progressq):
    xymax = int(math.sqrt(nmax)) + 1
    for x in range(1, xymax):
        for y in range(1, xymax):
            n = 3*x**2 - y**2
            if (x > y) and (n <= nmax) and (n % 12 == 11):
                q.put((n, 'flip'))
        progressq.put(('process3', x / (xymax - 1)))


def atkin4(nmax, q, progressq):
    xymax = int(math.sqrt(nmax)) + 1
    for n, is_prime in zip(range(xymax), check_table()):
        if n < 5:
            continue
        if is_prime:
            ik = 1
            while (ik * n**2 <= nmax):
                q.put((ik * n**2, 'reset'))
                ik += 1
        progressq.put(('process4', n / (xymax - 1)))


def atkin(nmax):
    with Manager() as manager:
        q = manager.Queue()
        progressq = manager.Queue()
        with Pool(5) as pool:
            writer = pool.apply_async(flipper, (nmax, q))
            pool.apply_async(watcher, (progressq,))

            j1 = pool.apply_async(atkin1, (nmax, q, progressq))
            j2 = pool.apply_async(atkin2, (nmax, q, progressq))
            j3 = pool.apply_async(atkin3, (nmax, q, progressq))

            j1.get()
            j2.get()
            j3.get()

            j4 = pool.apply_async(atkin4, (nmax, q, progressq))
            j4.get()

            q.put(None)
            writer.get()

    for n, is_prime in zip(range(nmax), check_table()):
        if n == 0 or n == 1 or n == 4:
            continue
        elif n == 2 or n == 3 or is_prime:
            yield n


if __name__ == '__main__':
    with open('primes.txt', 'w') as f:
        for n in atkin(int(sys.argv[1])):
            f.write(str(n) + '\n')
