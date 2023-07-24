'''

'''
import os
import math
from PIL import ImageOps
from PIL import Image, ImageDraw, ImageFont

# got idea from https://medium.com/@jtreitz/the-algorithm-for-a-perfectly-balanced-photo-gallery-914c94a5d8af


# start partition problem algorithm from https://stackoverflow.com/a/7942946
# modified to act on list of images rather than the weights themselves
# more info on the partition problem http://www8.cs.umu.se/kurser/TDBAfl/VT06/algorithms/BOOK/BOOK2/NODE45.HTM

from operator import itemgetter

def linear_partition(seq, k, dataList = None):
    if k <= 0:
        return []
    n = len(seq) - 1
    if k > n:
        return ([x] for x in seq)
    table, solution = linear_partition_table(seq, k)
    k, ans = k-2, []
    if dataList is None or len(dataList) != len(seq):
        while k >= 0:
            ans = [[seq[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
            n, k = solution[n-1][k], k-1
        ans = [[seq[i] for i in range(0, n+1)]] + ans
    else:
        while k >= 0:
            ans = [[dataList[i] for i in range(solution[n-1][k]+1, n+1)]] + ans
            n, k = solution[n-1][k], k-1
        ans = [[dataList[i] for i in range(0, n+1)]] + ans
    return ans

def linear_partition_table(seq, k):
    n = len(seq)
    table = [[0] * k for x in range(n)]
    solution = [[0] * (k-1) for x in range(n-1)]
    for i in range(n):
        table[i][0] = seq[i] + (table[i-1][0] if i else 0)
    for j in range(k):
        table[0][j] = seq[0]
    for i in range(1, n):
        for j in range(1, k):
            table[i][j], solution[i-1][j-1] = min(
                ((max(table[x][j-1], table[i][0]-table[x][0]), x) for x in range(i)),
                key=itemgetter(0))
    return (table, solution)

# end partition problem algorithm

def clamp(v,length,h):
    return length if v < length else h if v > h else v

# takes list of PIL image objects and returns the collage as a PIL image object
def makeCollage(imgList, spacing = 0, antialias = False, background=(0,0,0), aspectratiofactor = 0):
    # first downscale all images according to the minimum height of any image
#     minHeight = min([img.height for img in imgList])
#     if antialias:
#         imgList = [img.resize((int(img.width / img.height * minHeight),minHeight), Image.ANTIALIAS) if img.height > minHeight else img for img in imgList]
#     else:
#         imgList = [img.resize((int(img.width / img.height * minHeight),minHeight)) if img.height > minHeight else img for img in imgList]
        
    # first upscale all images according to the maximum height of any image (downscaling would result in a terrible quality image if a very short image was included in the batch)
    maxHeight = max([img.height for img in imgList])
    imgList = [(img.resize((int(img.width / img.height * maxHeight), maxHeight), Image.ANTIALIAS) if img.height < maxHeight else img) for img in imgList] if antialias else [(img.resize((int(img.width / img.height * maxHeight), maxHeight)) if img.height < maxHeight else img) for img in imgList]
    
    # generate the input for the partition problem algorithm
    # need list of aspect ratios and number of rows (partitions)
    [img.height for img in imgList]
    totalWidth = sum([img.width for img in imgList])
    avgWidth = totalWidth / len(imgList)
    targetWidth = avgWidth * math.sqrt(len(imgList) * aspectratiofactor)
    
    numRows = clamp(int(round(totalWidth / targetWidth)), 1, len(imgList))
    if numRows == 1:
        imgRows = [imgList]
    elif numRows == len(imgList):
        imgRows = [[img] for img in imgList]
    else:
        aspectRatios = [int(img.width / img.height * 100) for img in imgList]
    
        # get nested list of images (each sublist is a row in the collage)
        imgRows = linear_partition(aspectRatios, numRows, imgList)
    
        # scale down larger rows to match the minimum row width
        rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
        minRowWidth = min(rowWidths)
        rowWidthRatios = [minRowWidth / w for w in rowWidths]
        if antialias:
            imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio)), Image.ANTIALIAS) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
        else:
            imgRows = [[img.resize((int(img.width * widthRatio), int(img.height * widthRatio))) for img in row] for row,widthRatio in zip(imgRows, rowWidthRatios)]
    
    # pupulate new image
    rowWidths = [sum([img.width + spacing for img in row]) - spacing for row in imgRows]
    rowHeights = [max([img.height for img in row]) for row in imgRows]
    minRowWidth = min(rowWidths)
    w,h = (minRowWidth, sum(rowHeights) + spacing * (numRows - 1))
    
    if background == (0,0,0):
        background += (0,)
    else:
        background += (255,)
    outImg = Image.new("RGBA", (w,h), background)
    xPos,yPos = (0,0)
    
    for row in imgRows:
        for img in row:
            outImg.paste(img, (xPos,yPos))
            xPos += img.width + spacing
            continue
        yPos += max([img.height for img in row]) + spacing
        xPos = 0
        continue
    
    return outImg

# modified (significantly) from https://github.com/delimitry/collage_maker
# this main function is for the CLI implementation
def collage_maker(foldername, output_name, width,height,shuffle, gapsize, aspect_ratio, Name, Breed): #shuffle is 1 or zero.
    # def rgb(s):
    #     try:
    #         rgb = (0 if v < 0 else 255 if v > 255 else v for v in map(int, s.split(',')))
    #         return rgb
    #     except:
    #         raise argparse.ArgumentTypeError('Background must be (r,g,b) --> "(0,0,0)" to "(255,255,255)"')
    # parse = argparse.ArgumentParser(description='Photo collage maker')
    # parse.add_argument('-f', '--folder', dest='folder', help='folder with images (*.jpg, *.jpeg, *.png)', default=False)
    # parse.add_argument('-F', '--file', dest='file', help='file with newline separated list of files', default=False)
    # parse.add_argument('-o', '--output', dest='output', help='output collage image filename', default='collage.png')
    # parse.add_argument('-W', '--width', dest='width', type=int, help='resulting collage image height (mutually exclusive with --height)', default=5000)
    # parse.add_argument('-H', '--height', dest='height', type=int, help='resulting collage image height (mutually exclusive with --width)', default=5000)
    # parse.add_argument('-i', '--initheight', dest='initheight', type=int, help='resize images on input to set height', default=500)
    # parse.add_argument('-s', '--shuffle', action='store_true', dest='shuffle', help='enable images shuffle')
    # parse.add_argument('-g', '--gap-between-images', dest='imagegap', type=int, help='number of pixels of transparent space (if saving as png file; otherwise black or specified background color) to add between neighboring images', default=0)
    # parse.add_argument('-b', '--background-color', dest='background', type=rgb, help='color (r,g,b) to use for background if spacing is added between images', default=(255,255,255))
    # parse.add_argument('-c', '--count', dest='count', type=int, help='count of images to use', default=0)
    # parse.add_argument('-r', '--scale-aspect-ratio', dest='aspectratiofactor', type=float, help='aspect ratio scaling factor, multiplied by the average aspect ratio of the input images to determine the output aspect ratio', default=1.0)
    # parse.add_argument('-a', '--no-antialias-when-resizing', dest='noantialias', action='store_false', help='disable antialiasing on intermediate resizing of images (runs faster but output image looks worse; final resize is always antialiased)')

    if foldername:
        files = [os.path.join(foldername, fn) for fn in os.listdir(foldername)]
        images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
        for i in images:
            print(i)
        if "my_collage.png" in images:
            images.remove("my_collage.png")
        if "output.PNG" in images:
            images.remove("output.PNG")
        if "Addon.PNG" in images:
            images.remove("Addon.PNG")
    else:
        images = []

    # check if enough images are available
    if len(images) < 3:
        print("Need to use 3 or more images. Try again")
        exit(1)

    # shuffle images if needed
    # if shuffle:
    #     random.shuffle(images)
    # else:
    # images.sort()  # by filename

    # get PIL image objects for all the photos
    print('Loading photos...')
    pilImages = []
    for f in images:
        img = Image.open(f)
        # Need to explicitly tell PIL to rotate image if EXIF orientation data is present
        exif = img.getexif()
        # Remove all exif tags
        for k in exif:
            if k != 0x0112:
                exif[k] = None  # If I don't set it to None first (or print it) the del fails for some reason.
                del exif[k]
        # Put the new exif object in the original image
        new_exif = exif.tobytes()
        img.info["exif"] = new_exif
        # Rotate the image
        img = ImageOps.exif_transpose(img)
        if height > 2 and img.height > height:
            # if args.noantialias:
            #     pilImages.append(img.resize((int(img.width / img.height * args.initheight), args.initheight)))
            # else:
                pilImages.append(img.resize((int(img.width / img.height * height), height), Image.ANTIALIAS))
        else:
            pilImages.append(img)

    print('Making collage...')
    
    collage = makeCollage(pilImages, gapsize, None, (255,255,255), aspectratiofactor=aspect_ratio)
    
    if width > 0 and collage.width > width:
        collage = collage.resize((width, int(collage.height / collage.width * width)), Image.ANTIALIAS)
        pass
    elif height > 0 and collage.height > height:
        collage = collage.resize((int(collage.width / collage.height * height), height), Image.ANTIALIAS)
        pass
    
    collage.save(output_name)

    border_color = (255, 255, 255)  # Border color (default: black)
    border_width =gapsize//2  # Border width in pixels

    # Create a new image with increased dimensions for the border
    bordered_collage = Image.new("RGB", (collage.width + 2 * border_width, collage.height + 2 * border_width), border_color)

    # Paste the original collage onto the bordered image with an offset
    bordered_collage.paste(collage, (border_width, border_width))

    # Save the bordered collage
    bordered_collage.save(output_name)

    # Open the background image
    # background_image = Image.open("/tmp/my_collage.png")
    background_image = Image.open("/tmp/my_collage.png")

    draw = ImageDraw.Draw(background_image)

    # Set the corner radius and rectangle dimensions
    corner_radius = 20
    x1, y1 = background_image.width // 2 - 300, background_image.height // 2 - 80
    x2, y2 = background_image.width // 2 + 300, background_image.height // 2 + 80

    # Draw a rounded rectangle
    draw.rounded_rectangle([(x1, y1), (x2, y2)], corner_radius, fill="white")

    # overlay_image = Image.open("Addon.PNG")
    overlay_image = Image.open("/home/site/wwwroot/HorseFlask/misc/Addon.PNG")

    # Resize the overlay image to fit the rounded rectangle dimensions
    overlay_image = overlay_image.resize((x2 - x1 - 40, y2 - y1 -10 ))

    overlay_x = x1 + (x2 - x1) // 25
    overlay_y = y1

    # Paste the overlay image onto the base image at the specified position
    background_image.paste(overlay_image, (overlay_x, overlay_y), mask=overlay_image)

    # Add text to the overlay
    font = ImageFont.truetype("/home/site/wwwroot/HorseFlask/misc/arial.ttf", size=40)
    text = f"Name: {Name} \n Breed: {Breed}"
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((x1 + x2 - text_width) // 2 + 100, (y1 + y2 - text_height) // 2)
    draw.text(text_position, text, fill="black", font=font)

    # Save the resulting image
    # background_image.save( '/tmp/output.PNG')
    background_image.save("/tmp/output.PNG")

    print('Collage is ready!')

