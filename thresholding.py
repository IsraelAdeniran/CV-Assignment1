import numpy as np

def build_histogram(img):
    # make empty histogram (0-255)
    hist = np.zeros(256, dtype=np.int32)

    # loop through pixels
    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            # get grey level
            gl = int(img[x, y])
            # add to bin
            hist[gl] += 1

    return hist


def otsu_threshold(hist, total_pixels):
    # total sum of all intensities
    sum_all = 0.0
    for i in range(0, 256):
        sum_all += i * hist[i]

    # running totals for background
    sum_b = 0.0
    w_b = 0

    # best result so far
    best_t = 0
    best_var = -1.0

    # try every threshold 0..255
    for t in range(0, 256):

        # update background weight
        w_b += hist[t]
        if w_b == 0:
            continue

        # foreground weight
        w_f = total_pixels - w_b
        if w_f == 0:
            break

        # update background sum
        sum_b += t * hist[t]

        # means for both groups
        m_b = sum_b / w_b
        m_f = (sum_all - sum_b) / w_f

        # between class variance
        diff = m_b - m_f
        var_between = w_b * w_f * diff * diff

        # keep best threshold
        if var_between > best_var:
            best_var = var_between
            best_t = t

    return best_t

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