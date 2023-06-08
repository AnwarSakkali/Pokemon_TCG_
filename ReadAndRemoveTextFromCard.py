# 0. Start of script to have a card and remove the black text from the image
def removeTextFromCard():
    from PIL import Image, ImageDraw, ImageFont

    # Variables
    imageUrl = 'images/Calyrex.png' # get image from path
    convertedImageUrl = 'images/Filtered/convertedImage.png' # write converted image to path
    path = "images/Filtered/MaskedImage.png" # save masked image
    cardSize = (630, 880) # format of a pokemon card
    namebox_tl = (123, 29) # top left coordinates of namebox on the card
    movebox_tl = (37, 443) # top left coordinates of movebox on the card
    greyLimit = 150 # level of acceptance of grey colours
    overwriteValue = 150 # level of acceptance to write to either a or b
    a = (0, 0, 0) # empty tuple to be overwritten with another (grey) colour eventually 
    b = (0, 0, 0) # empty tuple to be overwritten with another (colourful) colour eventually

    # 1. Get a card and resize it
    im = Image.open(imageUrl).resize(cardSize).convert('RGB')
    im.show()

    # 2. Define boxes
    # 2A. namebox: 
    namebox_br = sumTuple(namebox_tl, (291, 50))
    nameFieldCrop = im.crop((*namebox_tl, *namebox_br))
    nameFieldDraw = ImageDraw.Draw(nameFieldCrop)

    # 3A. Tesseract for name
    Tesseract(nameFieldCrop)
    
    # 4A. Look for pixels in the crop.
    for y in range(nameFieldCrop.height):
        for x in range(nameFieldCrop.width):
            value = nameFieldCrop.getpixel((x, y))
            previousValue = nameFieldCrop.getpixel((x-1, y))
            greyValue = checkGreyValue(value)
            previousGreyValue = checkGreyValue(previousValue)

            # if the colour of the pixel is close to white/black, see how close the colour is to a or b
            # if colour is close to a or b, overwrite the current pixel with the closest of colour a or b respectively
            # if colour of the pixel is above the greylimit, do nothing and save colour for future usage
            if greyValue < greyLimit:
                if previousGreyValue < overwriteValue:
                    nameFieldCrop.putpixel((x, y), a)
                else:
                    nameFieldCrop.putpixel((x, y), b)
            else:
                if greyValue <= overwriteValue:
                    a = value
                else:
                    b = value

    # 5A. Write name in nametext
    nameFieldDraw.text((0, 5), "", font= ImageFont.truetype("arial.ttf", 50), fill=(0, 0, 0))
    im.paste(nameFieldCrop, namebox_tl)

    # -----------------------------------------------------------------------------------------------------

    # 2B. Movebox:
    movebox_br = sumTuple(movebox_tl,(550, 305))
    moveFieldCrop = im.crop((*movebox_tl, *movebox_br))
    moveFieldDraw = ImageDraw.Draw(moveFieldCrop)
    
    masking(moveFieldCrop, path)

    # 3B. Tesseract for movebox
    greyImage = moveFieldCrop.convert('L')
    Tesseract(greyImage)

    # Outcommented because it's now rewriting pixels of specific colours rather than putting a new box over it
    """draw.rectangle((movebox_tl, movebox_br), fill=(255, 255, 255))"""

    # 4B. Look for pixels in the crop. 
    for y in range(moveFieldCrop.height):
        for x in range(moveFieldCrop.width):
            value = moveFieldCrop.getpixel((x, y))
            previousValue = moveFieldCrop.getpixel((x-1, y))
            greyValue = checkGreyValue(value)
            previousGreyValue = checkGreyValue(previousValue)
            
            # if the colour of the pixel is close to white/black, see how close the colour is to a or b
            # if colour is close to a or b, overwrite the current pixel with the closest of colour a or b respectively
            # if colour of the pixel is above the greylimit, do nothing and save colour for future usage
            if greyValue < greyLimit:
                if previousGreyValue < overwriteValue:
                    moveFieldCrop.putpixel((x, y), a)
                else:
                    moveFieldCrop.putpixel((x, y), b)
            else:
                if greyValue <= overwriteValue:
                    a = value
                else:
                    b = value


    # 5B. Write movetext in movefield
    moveFieldDraw.text((0, 5), "", font= ImageFont.truetype("arial.ttf", 50), fill=(0, 0, 0))
    im.paste(moveFieldCrop, movebox_tl)

    # 6. Show image
    im = im.crop(im.getbbox())
    im.show()
    im.save(convertedImageUrl)

# Calculate bottom right
def sumTuple(tuple1, tuple2):
    if len(tuple1) == len(tuple2):
        return(x + y for x, y in zip(tuple1, tuple2))

# Return 0 to 255
# The lower, the blacker
def checkGreyValue(colourValue):
    avg = sum(colourValue[0:3]) / 3
    return avg
    
# Tesseract
def Tesseract(crop):
    from pytesseract import pytesseract
    path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    name = pytesseract.image_to_string(crop)
    print("name: ")
    print(name[:-1])

# uses tuple of rgb values to determine hex value
def rgb2hex(value):
    return '#%02x%02x%02x' % (value[0], value[1], value[2])

def masking(moveFieldCrop, path):
    from PIL import Image
    moveFieldMask = Image.new(mode="1", size=moveFieldCrop.size, color=0)
    
    for y in range(moveFieldCrop.height):
        for x in range(moveFieldCrop.width):
            try:
                value = moveFieldCrop.getpixel((x, y))
                value2 = moveFieldCrop.getpixel((x+1, y))
                value = sumTuple(value, value2)
            
                # find black pixels, make pixel and adjacent pixels white if so
                if (sum(list(value)[0:3]) /3 < 120):
                    moveFieldMask.putpixel((x, y), 1)
                    moveFieldMask.putpixel((x-1, y), 1)
                    moveFieldMask.putpixel((x+1, y), 1)
                    moveFieldMask.putpixel((x, y-1), 1)
                    moveFieldMask.putpixel((x, y+1), 1)
            except IndexError:
                pass

    moveFieldMask.save(path)
    return moveFieldMask

# Runtime
removeTextFromCard()