import numpy as np

def label_components(bw, connectivity=8):
    # make label image (0 = background)
    labels = np.zeros((bw.shape[0], bw.shape[1]), dtype=np.int32)

    # pick neighbours
    if connectivity == 4:
        neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:
        neighbours = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

    # label counter
    curlab = 0

    # store area per label
    areas = {}

    # scan image
    for i in range(0, bw.shape[0]):
        for j in range(0, bw.shape[1]):

            # start a new component
            if bw[i, j] == 255 and labels[i, j] == 0:
                curlab += 1
                areas[curlab] = 0

                # queue for bfs
                q = []
                q.append((i, j))
                labels[i, j] = curlab

                # flood fill
                while len(q) > 0:
                    y, x = q.pop(0)

                    # count pixels
                    areas[curlab] += 1

                    # check neighbours
                    for dy, dx in neighbours:
                        ny = y + dy
                        nx = x + dx

                        # stay in bounds
                        if ny < 0 or ny >= bw.shape[0] or nx < 0 or nx >= bw.shape[1]:
                            continue

                        # add unlabelled foreground
                        if bw[ny, nx] == 255 and labels[ny, nx] == 0:
                            labels[ny, nx] = curlab
                            q.append((ny, nx))

    return labels, areas

def largest_component_mask(labels, areas):
    # handle case with no components
    if len(areas) == 0:
        return np.zeros_like(labels, dtype=np.uint8), 0

    # find label with biggest area
    best_label = 0
    best_area = -1
    for lab in areas:
        if areas[lab] > best_area:
            best_area = areas[lab]
            best_label = lab

    # build mask image
    mask = np.zeros_like(labels, dtype=np.uint8)

    # keep only largest label
    for i in range(0, labels.shape[0]):
        for j in range(0, labels.shape[1]):
            if labels[i, j] == best_label:
                mask[i, j] = 255

    return mask, best_label


def count_holes(ring_mask):
    # invert ring so holes become white
    inv = 255 - ring_mask

    # label inverted image
    labels, areas = label_components(inv, 8)

    # count blobs that do not touch image edge
    hole_count = 0

    for lab in areas:
        touches_edge = False

        # check left and right edges
        for y in range(0, labels.shape[0]):
            if labels[y, 0] == lab or labels[y, labels.shape[1] - 1] == lab:
                touches_edge = True

        # check top and bottom edges
        for x in range(0, labels.shape[1]):
            if labels[0, x] == lab or labels[labels.shape[0] - 1, x] == lab:
                touches_edge = True

        # blobs not touching the edge are holes
        if not touches_edge:
            hole_count += 1

    return hole_count