#!/usr/bin/env python
#
# Custom Bingo Game Generation
# Have you ever wanted to make your own simple bingo-style game with custom
# images?  If so, look not much further!  This script helps you create
# multiple boards and games from a set of input images including the "random draw"
# feature for calling games.
#
# Created 12/21/17 - ezavesky

import os.path
from PIL import Image, ImageFont, ImageDraw
import random


def file_fetch(dirRoot, gameName):
    """File fetch for content in a directory, keeping single-letter prefixes"""
    import re
    filelist_raw = [f for f in os.listdir(dirRoot) if os.path.isfile(os.path.join(dirRoot, f))]
    fileset = {}
    reFile = re.compile(r"^([{:}])_.*".format(gameName))
    for f in filelist_raw:
        objMatch = reFile.search(f)
        if objMatch is not None:
            if objMatch.group(1) not in fileset:
                fileset[objMatch.group(1)] = []
            fileset[objMatch.group(1)].append([0, os.path.join(dirRoot, objMatch.group(0))])
    return fileset


def image_paste_center(montage, image, cellSize, x, y, scaleFirst=False):
    if scaleFirst:  # make incoming image as large as possible for cell?
        if image.width > image.height:
            image = image.resize((cellSize, (int)(image.height / image.width * cellSize)), Image.ANTIALIAS)
        else:
            image = image.resize(((int)(image.width / image.height * cellSize), cellSize), Image.ANTIALIAS)
    x = (int)((cellSize - image.width) / 2 + x)
    y = (int)((cellSize - image.height) / 2 + y)
    montage.paste(image, (x, y))


def generate_montage(fileSet, fileFree, nameFile, colKeys=None,
                     cellSize=200, cellCount=5, marginSize=20, cardNumber=None):
    # images = [Image.open(filename) for filename in filenames]
    # width = max(image.size[0] + margin for image in images)*row_size
    # height = sum(image.size[1] + margin for image in images)
    colorBack = (255, 255, 255, 0)
    colorText = (0, 0, 0, 255)
    montage = Image.new(mode='RGBA', size=((cellSize + marginSize) * (cellCount),
                                           (cellSize + marginSize) * (cellCount + 1)), color=colorBack)

    # font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", 16)
    # font = ImageFont.load_default()
    font = ImageFont.truetype("arial.ttf", 100)

    idxCenter = (int)(cellCount / 2)
    offset_x = (int)(marginSize / 2)
    if colKeys is None:
        colKeys = list(fileSet.keys())
    for i in range(min(len(colKeys), cellCount)):  # iterate ove rcolumns
        offset_y = marginSize / 2

        # formulate the name for the card...
        text = colKeys[i].title()
        text_x, text_y = font.getsize(text)
        image = Image.new(mode='RGBA', size=(text_x, text_y), color=colorBack)
        draw = ImageDraw.Draw(image)
        # draw.font_family = "Helvetica"
        # draw.font_size = 100
        draw.text((0, 0), text, font=font, fill=colorText)
        image_paste_center(montage, image, cellSize, offset_x, offset_y, True)

        # draw.text((offset_x, offset_y), text, fill=colorText)
        offset_y = (int)(offset_y + cellSize + marginSize)  # walk to next row

        for j in range(cellCount):  # iterate over rows
            # print("[{:},{:},{:},{:}x{:}]: {:}".format(i, j, colKeys[i], offset_x, offset_y, fileSet[colKeys[i]][j][1]))

            if i == j and i == idxCenter and fileFree is not None:
                image = Image.open(fileFree)  # grab filename
            else:
                image = Image.open(fileSet[colKeys[i]][j][1])  # grab filename
            image.thumbnail((cellSize, cellSize), Image.ANTIALIAS)  # generating the thumbnail from given size

            fileSet[colKeys[i]][j][0] += 1  # increment count
            image_paste_center(montage, image, cellSize, offset_x, offset_y)

            # draw = ImageDraw.Draw(montage)
            # draw.rectangle(((offset_x - marginSize / 2, offset_y - marginSize / 2),
            #                (cellSize, cellSize)), outline=colorText)

            offset_y = (int)(offset_y + cellSize + marginSize)  # walk to next row
        offset_x = (int)(offset_x + cellSize + marginSize)
        random.shuffle(fileSet[colKeys[i]])  # shuffle list initially
        sorted(fileSet[colKeys[i]], key=lambda x: x[0])  # sort by lowest number

    # now formulate the card number (for reference)
    if cardNumber is not None:
        textCard = "card #{:}".format(cardNumber)
        font = ImageFont.truetype("arial.ttf", 20)
        text_x, text_y = font.getsize(textCard)
        draw = ImageDraw.Draw(montage)
        draw.text((montage.width - text_x, 0), textCard, font=font, fill=colorText)

    # montage = montage.crop((0, 0, max_x, max_y))
    montage.save(nameFile)


def generate_games(fileSet, nameFile, numGame=1, joinChar="  "):
    filesFlat = []
    maxLen = 0
    for i in fileSet:
        for f in fileSet[i]:
            fileClean = os.path.splitext(os.path.basename(f[1]))[0]
            filesFlat.append(fileClean)
            maxLen = max(len(fileClean), maxLen)
    linesOutput = [['{0:<{1}}'.format(n + 1, 6)] for n in range(len(filesFlat))]
    linesOutput.insert(0, ["{0:<{1}}".format("item", 6)])
    for g in range(numGame):
        random.shuffle(filesFlat)  # shuffle list initially
        linesOutput[0].append("{0:<{1}}".format("game {:}".format(g), maxLen))
        for n in range(len(filesFlat)):
            linesOutput[n + 1].append("{0:<{1}}".format(filesFlat[n], maxLen))
    fO = open(nameFile, 'wt')
    for l in linesOutput:
        fO.write(joinChar.join(l) + "\n")
    fO.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="A simple script for generating bingo-style game boards")
    parser.add_argument('-d', '--dir_images', type=str, default=os.getcwd(), help="Path for input images.")
    parser.add_argument('-n', '--game_name', type=str, default='bingo', help="Name for header row (e.g. 'bingo'), must match prefix of image files")
    parser.add_argument('-c', '--card_count', type=int, default=30, help="How many card files should be generated?")
    parser.add_argument('-g', '--game_count', type=int, default=6, help="How many game listings should be generated?")
    parser.add_argument('-G', '--game_file', type=str, default='games.txt', help="Destination for game file in text")
    parser.add_argument('image_free', type=str, help="Absolute path to 'free' image for center board")
    config = vars(parser.parse_args())  # pargs, unparsed = parser.parse_known_args()

    if not config['image_free']:
        print("Sorry, you must provide a 'free image' path for the center square.")
        return -1

    fileSet = file_fetch(config['dir_images'], config['game_name'])

    print("Creating {:} games in {:}...".format(config['game_count'], config['game_file']))
    generate_games(fileSet, config['game_file'], config['game_count'])
    for c in range(config['card_count']):
        cardFile = 'card{:}.png'.format(c)
        print("Creating card {:} in {:}...".format(c, cardFile))
        generate_montage(fileSet, config['image_free'], cardFile, config['game_name'], cardNumber=c)
    print("All done!")


if __name__ == '__main__':
    main()
