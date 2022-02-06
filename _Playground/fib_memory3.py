def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    cache = {0: 0, 1: 1}
    def fib(_n):
        if _n in cache:
            return cache[_n]
        else:
            cache[_n] = fib(_n - 1) + fib(_n - 2)
            print(cache)
            return fib(_n - 1) + fib(_n - 2)
    return fib(nth_nmb)

print((fibonacci_recursive(20)))