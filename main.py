import cv2 as cv
import time
import os
from thresholding import build_histogram, otsu_threshold, threshold
from morphology import closing
from ccl import label_components, largest_component_mask, count_holes

# loop through o-ring images
for i in range(1, 16):

    # build file path
    path = os.path.join("data", "Oring" + str(i) + ".jpg")

    # read as grayscale
    img = cv.imread(path, 0)

    # skip missing images
    if img is None:
        print("Could not load:", path)
        continue

    # start timer
    before = time.time()

    # build histogram
    hist = build_histogram(img)

    # get otsu threshold
    total = img.shape[0] * img.shape[1]
    thresh_val = otsu_threshold(hist, total)

    # threshold image
    bw = threshold(img, thresh_val)

    # invert so ring becomes 255
    bw = 255 - bw

    # close small holes
    bw = closing(bw, 1)

    # label regions
    labels, areas = label_components(bw, 8)

    # keep only the biggest region
    ring_mask, ring_label = largest_component_mask(labels, areas)

    # count holes in the ring
    holes = count_holes(ring_mask)

    # pass fail check
    if holes == 1:
        result = "PASS"
    else:
        result = "FAIL"

    # end timer
    after = time.time()
    t = after - before

    # convert for drawing
    rgb = cv.cvtColor(ring_mask, cv.COLOR_GRAY2RGB)

    # create bigger canvas so text does not cover ring
    canvas = cv.copyMakeBorder(
        rgb,
        150, 50,
        50, 50,
        cv.BORDER_CONSTANT,
        value=(0, 0, 0)
    )

    # add image number
    cv.putText(canvas, "Image: " + str(i), (20, 40),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # add time
    cv.putText(canvas, "Time: " + str(round(t, 4)) + "s", (20, 80),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # add result
    cv.putText(canvas, "Result: " + result, (20, 120),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)


    # show result
    cv.imshow("ring mask", canvas)
    cv.waitKey(0)

cv.destroyAllWindows()