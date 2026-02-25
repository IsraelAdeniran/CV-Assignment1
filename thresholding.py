def threshold(img, thresh):
    # make a binary copy
    bw = img.copy()

    # loop through pixels
    for x in range(0, bw.shape[0]):
        for y in range(0, bw.shape[1]):
            if bw[x, y] > thresh:
                bw[x, y] = 255
            else:
                bw[x, y] = 0

    return bw