import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# CAP_PROP_FRAME_WIDTH = Width of the frames in the video stream.
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# FourCC is a 4-byte code used to specify the video codec
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

# Writes the video to a file
# cv.VideoWriter(	filename, fourcc, fps, frameSize[, isColor]
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (480, 480))

# cap.read() returns a bool (True/False). If the frame is read correctly, it will be True.
# So you can check for the end of the video by checking this returned value.
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# The shape of an image is accessed by img.shape.
# It returns a tuple of the number of rows, columns, and channels (if the image is color)
print(frame1.shape)
# You can check whether the capture is initialized or not using cap.isOpened()
while cap.isOpened():

    # absdiff: Absolute difference between two arrays when they have the same size and type
    diff = cv2.absdiff(frame1, frame2)
    # Converts an image from one color space to another.
    # In this case, diff is being converted to COLOR_BGR2GRAY
    # COLOR_BGR2GRAY is a color conversion code
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blurs an image using Gaussian Blur
    # This takes 6 parameters, but only 3 is used:
    # src: The input image
    # ksize: The Gaussian Kernel size(ksize.width, ksize.height). They must be positive and odd
    # sigmaX: Gaussian kernel standard deviation in X direction. Because sigmaX is 0, sigmaY is also 0.
    # if both sigmas are zeros, they are computed from ksize.width and ksize.height, respectively.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).
    # The method returns two outputs. The first is the threshold that was used and the second output is the thresholded image.
    # First Argument: Source Image(Should be a grayscale image)
    # Second Argument: The threshold value used to classify the pixel values
    # Third Argument: The maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value.
    # 4: The type of thresholding you wish to use
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    ''' a kernel is a set of weights, which determine how each output pixel is calculated from a neighborhood of input pixels.
    Another term for a kernel is a convolution matrix. It mixes up or convolves the pixels in a region.
    Similarly, a kernel-based filter may be called a convolution filter.'''
    '''Erosion: As the kernel is scanned over the image, we compute the minimal pixel value overlapped by the kernel
    and replace the image pixel under the anchor point with that minimal value.'''
    # As a result, the bright areas of the image get thinner, whereas the dark zones gets bigger.
    # First Argument: Source Image
    # Second Argument: Kernel used to perfrom the operation. If not specified, the default is a 3x3 matrix
    # Third Argument: Allows you to perform multiple erosions(iterations at once.
    erode = cv2.erode(thresh.copy(), None, iterations=5)

    # This is the exact opposite of erosion. Take the definition used above for erosion and replace "minimal" to "maximal"
    dilated = cv2.dilate(erode, None, iterations=5)

    # Contours can be explained simply as a curve joining all the continuous points (along the boundary), having same color or intensity.
    # The contours are a useful tool for shape analysis and object detection and recognition.
    # In OpenCV, finding contours is like finding white object from black background.
    # So remember, object to be found should be white and background should be black.
    # The function retrieves contours from the binary image using the algorithm
    # First Parameter: The source image
    # Second Parameter: Contour retrieval mode(RETR_TREE: retrieves all of the contours and reconstructs a full hierarchy of nested contours.)
    # Third Parameter: Contour approximation method(compresses horizontal, vertical, and diagonal segments and leaves only their end points.
    # For example, an up-right rectangular contour is encoded with 4 points.)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # cv2.contourArea: Calculates a contour area.
        c = max(contours, key=cv2.contourArea)
        '''The cv2.boundingRect() function of OpenCV is used to draw an approximate rectangle around the binary image.
        This function is used mainly to highlight the region of interest after obtaining contours from an image.'''
        (x, y, w, h) = cv2.boundingRect(c)
        # cv2.rectangle: Used to draw a rectangle on any image
        # First Parameter: It is the image on which rectangle is to be drawn.
        # Second and Third Parameters: Starting and ending coordinates of the rectangle respectively.(X,Y)
        # Fourth Parameter: Color of borderline
        # Fifth Parameter: Thickness of Rectangle
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText: Used to draw a text string on any image
        # First Parameter: It is the image on which text is to be drawn.
        # Second Parameter: Text String to be drawn
        # Third Parameter: It is the coordinates of the bottom-left corner of the text string in the image.
        # The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
        # Fourth Parameter: Font
        # Fifth Parameter: Font scale factor that is multiplied by the font-specific base size.
        # 6: Color
        # 7: Thickness
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    # Resizes image (height, width)
    image = cv2.resize(frame1, (720, 480))

    # Write the image(frame) into the file 'output.avi'
    out.write(image)
    # Display the resulting frame
    cv2.imshow("feed", image)
    frame1 = frame2
    _, frame2 = cap.read()

    # Press Q on keyboard to stop recording
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Closes all the frames
cv2.destroyAllWindows()
# When everything's done, release the video capture and video write objects
cap.release()
out.release()
