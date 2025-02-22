"""
PROBLEM DESCRIPTION. Consider an image of NxM pixels with each pixel colored
black or white (1 or 0 if you will). The task is to find all clusters of
pixels colored in a particular color. The cluster is defined as a group of
pixels(>0) having the same color, and neighboring horizontally, vertically or
diagonally. For example,

|* *   |    The bottom left 2 pixels have coordinates (0,0) and (0,1). They
|**   *|    form a group because they are connected horizontally. To the
|** *  |    right, at position (0,3) there's another pixel. It too forms
|      |    a group, and this group contains only one pixel. At the top left
|** *  |    corner, 6 pixels form a group, namely (2,0), (2,1), (3,0), (3,1),
            (4,0) and (4,2). Finally, pixels (2,3) and (3,5) form two separate
            groups with one pixel only, as they are not connected to any other
            pixel. (see positions variable under __main__ to define this figure)

Consider coordinates of pixels as integers. We'll call pixels i and j
neighboring, when one of the two holds, or both:
    1) |x_i - x_j| = 1, (i!=j)
    2) |y_i - y_j| = 1, (i!=j)

Note: the data is given w.r.t. one of the colors (black, say). Think of those
stars above as black and the rest is white. For example, the point (1,0) is
is not given (it's white). So we're interested in all black clusters on the
white canvas.

Q: Find all groups.

ALGORITHM DESCRIPTION. Consider a point anywhere on the image. A point may
or may not have neighbors. This is of course easy to check; just look around
in all directions: north, northeast, east, ... northwest (8 directions) and
see if those points belong to our given image.

Now comes the tricky part. Recursion. The function find_neighbors(point) does
all the dirty job - it recursively traverses every neighboring point and
marks the traversed pixels. Additionally, it also masks parent's neighbors
from the child's to prevent this:

|***| Select bottom left node (0,0). Its neighbors are (1,0), (0,1) and (1,1)
|***| Make recursive call w/ f.e. node (1,0). The node (1,0) sees the nodes
|***| at the top, to the right, but also the nodes that the upper stack
      frame (i.e. parent) has already seen. So we mask them away using the
      second argument 'ignore'

The base case of the recursion (a terminating condition) is that eventually
all nodes will be either traversed (and marked in 'seen_before') variable or
masked away by the parent stack frame. For example a node 'i' may have
6 neighbors, but the actual 'neighbors' variable will be an empty set, because
other stack frames handled those particular points, because they were also
neighbors to some other points. Note, masking is important here also because
it prevents making unnecessary calls. Ignoring parent's neighbors is good
from algorithmical standpoint. Note, find_neighbors() doesn't return
anything, it only works through side-effects

The loop in __main__ is simple: a given image is stored in 'positions'
variable. Because the groups are independent, we can just remove the
just-found group from the 'positions' using remove_group(). Eventually
'positions' becomes an empty set and the whole thing terminates.

"""


def parse(path):
    coords = []
    with open(path, 'r') as f:
        for num_lines, line in enumerate(f, 1):
            tmp = line.split()
            coords.append((int(tmp[0]), int(tmp[1])))
    return coords


def remove_group(gr):
    global positions
    positions = list(set(positions) - set(gr))


def find_increment(key):
    if key is 'n':
        dx, dy = 0, 1
    elif key is 'ne':
        dx, dy = 1, 1
    elif key is 'e':
        dx, dy = 1, 0
    elif key is 'se':
        dx, dy = 1, -1
    elif key is 's':
        dx, dy = 0, -1
    elif key is 'sw':
        dx, dy = -1, -1
    elif key is 'w':
        dx, dy = -1, 0
    elif key is 'nw':
        dx, dy = -1, 1
    else:
        raise ValueError("I don't know why I throw")
    return dx, dy


def next_neighbor(point, direc):
    x, y = point[0], point[1]
    dx, dy = find_increment(direc)
    return (x + dx, y + dy)


def is_neighbor(point):
    return point in positions


def get_neighbors(point):
    all_neighbors = []
    for direc in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
        next_point = next_neighbor(point, direc)
        if is_neighbor(next_point):
            all_neighbors.append(next_point)
    return all_neighbors


def find_neighbors(point, ignore=None):
    if ignore is None:
        ignore = []
    seen_before.append(point)
    neighbors = get_neighbors(point)

    for neighbor in neighbors:
        if neighbor not in seen_before and neighbor not in ignore:
            find_neighbors(neighbor, ignore=neighbors)


if __name__ == '__main__':
    ## TO IVANA: This is for testing. You can draw these points yourself
    # and convince yourself that the code works.
    positions = [
            (0,0),
            (0,1),
            (0,3),
            (2,0),
            (2,1),
            (2,3),
            (3,0),
            (3,1),
            (4,0),
            (4,2),
            (3,5)
            ]

    ## TO IVANA: uncomment the line below to parse your file. I store
    ## your data in the same way as 'positions' variable above, i.e.
    ## a list of tuples, each tuple is (x,y)

    #positions = parse('12N_black.dat') 

    seen_before = []
    groups = []
    while positions:
        pivot = positions[0]
        find_neighbors(pivot)
        groups.append(seen_before.copy())
        remove_group(seen_before)
        seen_before.clear()

    for group in groups:
        print(group)
