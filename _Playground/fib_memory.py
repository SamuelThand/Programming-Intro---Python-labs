def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""
    def fib_mem(_n):
        cache = {0: 0, 1: 1}
        if _n not in cache:
            cache[_n] = fib_mem(_n - 1) + fib_mem(_n - 2)
            print(cache)
            return cache[_n]
        else:
            return cache[_n]
    return fib_mem(nth_nmb)

print((fibonacci_memory(20)))