# https://yangcha.github.io/iview/iview.html --> Pixel Identifier
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime,os
def fileDel(x):
    # Deletes the passed file.
    if os.path.exists(x):
        os.remove(x)
        print('Deleted')
    else:
        print("The file does not exist")
# Open an Image
img = Image.open('ticketpages/1.png')

txt_1=input('Enter Place:')
# Call draw Method to add 2D graphics in an image
I1 = ImageDraw.Draw(img)
title_font = ImageFont.truetype('Playfair_Display/f2.ttf', 50)
# Add Text to an image
I1.text((794,31), txt_1, (0,0,0), font=title_font)
# Display edited image
img.show()


# Save the edited image
img.save("s1.png")


fileDel('s1.png')