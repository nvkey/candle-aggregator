from time import sleep, time


def foo(delay=1.5):
    # sleep(delay)
    # print(f'sleeping for {delay} seconds')
    ...


foo()


def solve(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        res = func(*args, **kwargs)
        solve = time() - t1
        print(solve)
        return res

    return wrapper


@solve
def bar(delay_from_start=1.5):
    sleep(delay_from_start)
    print(f"sleeping for {delay_from_start} seconds")
    return "bar closed"


a = bar()
print(a)
assert a == 'bar closed'