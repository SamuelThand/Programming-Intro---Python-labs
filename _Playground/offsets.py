import itertools

offsets = [-1, 1, 0]
for item in itertools.product(offsets, offsets):
    print(item)