import numpy as np

def label_components(bw, connectivity=8):
    # make label image (0 = background)
    labels = np.zeros((bw.shape[0], bw.shape[1]), dtype=np.int32)

    # pick neighbours
    if connectivity == 4:
        neighbours = [(-1,0),(1,0),(0,-1),(0,1)]
    else:
        neighbours = [(-1,-1),(-1,0),(-1,1),
                      (0,-1),        (0,1),
                      (1,-1),(1,0),(1,1)]

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