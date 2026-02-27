def dilate(img, num_levels):
    # run dilation multiple times
    for level in range(num_levels):

        # start from a fresh copy each pass
        out = img.copy()

        # 8 neighbours
        neighbours = [(-1,-1),(-1,0),(-1,1),
                      (0,-1),        (0,1),
                      (1,-1),(1,0),(1,1)]

        # scan inner pixels (avoid edges)
        for i in range(1, img.shape[0]-1):
            for j in range(1, img.shape[1]-1):

                # only change background pixels
                if img[i, j] == 0:
                    toDilate = False

                    # check neighbours for foreground
                    for y, x in neighbours:
                        if img[i+y, j+x] == 255:
                            toDilate = True

                    # set to foreground if any neighbour is foreground
                    if toDilate:
                        out[i, j] = 255

        # move to next pass
        img = out

    return out