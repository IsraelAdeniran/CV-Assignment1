import cv2 as cv
import time
import os
from thresholding import threshold

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

    # threshold image
    thresh = 100
    bw = threshold(img, thresh)

    # end timer
    after = time.time()
    t = after - before

    # convert for drawing
    rgb = cv.cvtColor(bw, cv.COLOR_GRAY2RGB)

    # add simple text
    cv.putText(rgb, "Image: " + str(i), (20, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv.putText(rgb, "Time: " + str(round(t, 4)) + "s", (20, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # show result
    cv.imshow("thresholded image", rgb)
    cv.waitKey(0)

cv.destroyAllWindows()