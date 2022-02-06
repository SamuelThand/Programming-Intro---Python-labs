item = (2,3)
_cell_coord = (1,3)

for value in zip(item, _cell_coord):
    sum(value)
    print(value)

item = tuple(sum(value) for value in zip(item, _cell_coord))
#
print(item)

print(sum((1,2),(4,3)))