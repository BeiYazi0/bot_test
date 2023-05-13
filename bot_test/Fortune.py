import os
import json
import random

from PIL import Image, ImageDraw, ImageFont


_dir = os.getcwd() + '\\pcr-fortune\\'
fontPath = {
        "title": _dir + "font/Mamelon.otf",
        "text": _dir + "font/sakura.ttf",
    }

def randomBasemap():
    p = _dir + "img"
    return p + "/" + random.choice(os.listdir(p))

def readJsonFile(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.loads(f.read())

def copywriting():
    p = _dir +"fortune/copywriting.json"
    content = readJsonFile(p)
    return random.choice(content["copywriting"])

def getTitle(structure):
    p = _dir + "fortune/goodLuck.json"
    content = readJsonFile(p)
    for i in content["types_of"]:
        if i["good-luck"] == structure["good-luck"]:
            return i["name"]
    raise Exception("Configuration file error")

def decrement(text):
    length = len(text)
    result = []
    cardinality = 9
    if length > 4 * cardinality:
        return [False]
    numberOfSlices = 1
    while length > cardinality:
        numberOfSlices += 1
        length -= cardinality
    result.append(numberOfSlices)
    # Optimize for two columns
    space = " "
    length = len(text)
    if numberOfSlices == 2:
        if length % 2 == 0:
            # even
            fillIn = space * int(9 - length / 2)
            return [
                numberOfSlices,
                text[: int(length / 2)] + fillIn,
                fillIn + text[int(length / 2) :],
            ]
        else:
            # odd number
            fillIn = space * int(9 - (length + 1) / 2)
            return [
                numberOfSlices,
                text[: int((length + 1) / 2)] + fillIn,
                fillIn + space + text[int((length + 1) / 2) :],
            ]
    for i in range(0, numberOfSlices):
        if i == numberOfSlices - 1 or numberOfSlices == 1:
            result.append(text[i * cardinality :])
        else:
            result.append(text[i * cardinality : (i + 1) * cardinality])
    return result

def vertical(content):
    lst = []
    for s in content:
        lst.append(s)
    return "\n".join(lst)

def drawing():
    imgPath = randomBasemap()
    img = Image.open(imgPath)
    # Draw title
    draw = ImageDraw.Draw(img)
    text = copywriting()
    title = getTitle(text)
    text = text["content"]
    font_size = 45
    color = "#F5F5F5"
    image_font_center = (140, 99)
    ttfront = ImageFont.truetype(fontPath["title"], font_size)
    font_length = ttfront.getbbox(title)
    draw.text(
        (
            image_font_center[0] - font_length[2] / 2,
            image_font_center[1] - font_length[3] / 2,
        ),
        title,
        fill=color,
        font=ttfront,
    )
    # Text rendering
    font_size = 25
    color = "#323232"
    image_font_center = [140, 297]
    ttfront = ImageFont.truetype(fontPath["text"], font_size)
    result = decrement(text)
    if not result[0]:
        return
    textVertical = []
    for i in range(0, result[0]):
        font_height = len(result[i + 1]) * (font_size + 4)
        textVertical = vertical(result[i + 1])
        x = int(
            image_font_center[0]
            + (result[0] - 2) * font_size / 2
            + (result[0] - 1) * 4
            - i * (font_size + 4)
        )
        y = int(image_font_center[1] - font_height / 2)
        draw.text((x, y), textVertical, fill=color, font=ttfront)
    # Save
    outPath = _dir+'output.png'
    img.save(outPath)


