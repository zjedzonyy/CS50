import sys
import random
from pyfiglet import Figlet


fontIsRandom = False

if(len(sys.argv) == 1):
    fontIsRandom = True
elif(len(sys.argv) == 3):
    fontIsRandom = False
else:
    sys.exit("WRONG ")


figlet = Figlet()

availableFonts = figlet.getFonts()

if fontIsRandom == False:
    if(sys.argv[1] not in ["-f", "--font"]):
        sys.exit("ERROR ")
    try:
        font = figlet.setFont(font=sys.argv[2])
    except:
        sys.exit("Font Doesn't Exist ")
else:
    font = random.choice(availableFonts)
print(font)

txt = input("Input: ")
print(figlet.renderText(txt))