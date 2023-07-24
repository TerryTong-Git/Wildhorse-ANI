import imquality.brisque as brisque
from skimage import io, img_as_float

#score based on sharpness
# img = cv2.imread("./test3.jpg",1)
# iqa = DOM()
# score1 = iqa.get_sharpness(img)
# print("score for 1 is", score1)

#Need to change dependencies
# Also turn of multichannel
# Only convert image to grayscale if RGB
# if self.image.shape[-1] == 3:
#     self.image = skimage.color.rgb2gray(self.image) on line 45 of brisque.py
def quality(binary_image):
    image = img_as_float(io.imread(binary_image, as_gray=True))
    score = brisque.score(image)
    return score

#tensorflow has some deployment error, so choosing tensorflow-cpu instead

# I have chosen to use Brisque over Image quality by sharpness estimation because it is trained on a natural scenery and is perfect for this context as it takes into account blur, distortions, realisticness etc. 
# Sharpness will give good scores to things like drawings which are not realistic but have sharp edges. 