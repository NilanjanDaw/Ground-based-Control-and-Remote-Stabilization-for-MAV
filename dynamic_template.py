import cv2
import numpy as np
import itertools
import time
from scipy import spatial

cap = cv2.VideoCapture(0)  # Setting webcam for video capture
fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fontScale = 1
thickness = 1
template_image = ()

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, image, template_image

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)
        crop = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        template_image = crop
        cv2.imshow("image_crop", template_image)

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)


def template_match(image):
    f = open("standard deviation.txt", "a")
    global template_image
    res = cv2.matchTemplate(image,template_image,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    h, w, _ = template_image.shape
    bottom_right = (max_loc[0] + w, max_loc[1] + h)
    cv2.rectangle(image,max_loc, bottom_right, 255, 2)
    cv2.imshow("image", image)
    template_image_new = image[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]
    manhattan_deviation = np.sum(template_image - template_image_new)
    print "Manhattan " + str(manhattan_deviation)
    euclidean_deviation = np.sqrt(np.sum(np.square(template_image - template_image_new)))
    print "Euclidean " + str(euclidean_deviation)
    standard_deviation = np.sqrt(np.sum(np.square(template_image - template_image_new)) / np.size(template_image))
    print "Standard " + str(standard_deviation)

    mean = np.mean(template_image, axis=0)
    mean, eigenVector = cv2.PCACompute(template_image, mean).reshape(1, -1)
    print eigenVector
    template_image = template_image_new
    cv2.imwrite("templates/template_picture" + str(time.time()) + ".jpg", template_image, params=[])
    f.write(str(standard_deviation) + "\n")
    cv2.imshow("image_crop", template_image)
    f.close()
    return 0


def Sift(image):
    img = ()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT()
    kp = sift.detect(image,None)
    img = cv2.drawKeypoints(image,kp, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('sift_keypoints.jpg', img)
    return 0


def findKeyPoints(img, template, distance=200):
    detector = cv2.FeatureDetector_create("SIFT")
    descriptor = cv2.DescriptorExtractor_create("SIFT")

    skp = detector.detect(img)
    skp, sd = descriptor.compute(img, skp)

    tkp = detector.detect(template)
    tkp, td = descriptor.compute(template, tkp)

    flann_params = dict(algorithm=1, trees=4)
    flann = cv2.flann_Index(sd, flann_params)
    idx, dist = flann.knnSearch(td, 1, params={})
    #idx, dist = RandomForestClassifier(td,n_estimators=10,max_depth=10)
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    skp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            skp_final.append(skp[i])

    flann = cv2.flann_Index(td, flann_params)
    idx, dist = flann.knnSearch(sd, 1, params={})
    del flann

    dist = dist[:,0]/2500.0
    dist = dist.reshape(-1,).tolist()
    idx = idx.reshape(-1).tolist()
    indices = range(len(dist))
    indices.sort(key=lambda i: dist[i])
    dist = [dist[i] for i in indices]
    idx = [idx[i] for i in indices]
    tkp_final = []
    for i, dis in itertools.izip(idx, dist):
        if dis < distance:
            tkp_final.append(tkp[i])

    return skp_final, tkp_final


def drawKeyPoints(img, template, skp, tkp, num=-1):
    h1, w1 = img.shape[:2]
    h2, w2 = template.shape[:2]
    nWidth = w1+w2
    nHeight = max(h1, h2)
    hdif = (h1-h2)/2
    newimg = np.zeros((nHeight, nWidth, 3), np.uint8)
    newimg[hdif:hdif+h2, :w2] = template
    newimg[:h1, w2:w1+w2] = img

    maxlen = min(len(skp), len(tkp))
    if num < 0 or num > maxlen:
        num = maxlen
    for i in range(num):
        pt_a = (int(tkp[i].pt[0]), int(tkp[i].pt[1]+hdif))
        pt_b = (int(skp[i].pt[0]+w2), int(skp[i].pt[1]))
        cv2.line(newimg, pt_a, pt_b, (255, 0, 0))
    return newimg


while True:
    # display the image and wait for a keypress
    _, image = cap.read()
    cv2.imshow("image", image)
    if len(template_image) > 0:
        #skp, tkp = findKeyPoints(image, template_image, 200)
        #newimg = drawKeyPoints(image, template_image, skp, tkp, -1)
        #cv2.imshow("im", newimg)
        template_match(image=image)
    else:
        Sift(image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# close all open windows
cv2.destroyAllWindows()