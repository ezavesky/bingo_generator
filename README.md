# Custom Bingo Game Generation
Have you ever wanted to make your own simple bingo-style game with custom
images?  If so, look not much further!  This script helps you create
multiple boards and games from a set of input images including the "random draw"
feature for calling games.

# Creating your game
Just follow these steps and you'll get a set of card images and a textual
game file with random draws.

## Downloading Images
First, you'll need to source the images for your board.   Head over to your
favorite search engine and begin finding the ideal images for your board.
The underlying image library is pretty robust, so you should be able to use
most image input types (e.g. `.png`, `.jpg`, etc.).

The script assumes a 5x5 board layout, so getting a minimum of `40` images
should provide enough for some board diversity.  The more images you collect
the harder (or longer) a game will run.

## Renaming Images
After you have your images, you'll need to rename them to have a single-letter
prefix.  For example, if your game is names `bingo` you will need to rename
all images to have either a `b_`, `i_`, `n_`, `g_`, or `o_` prefix.  Be mindful
of how many images are under each prefix, because this is how the game
randomly generates the content for each board.  The program allows you to use
other names (other than `bingo`), but generally the 5x5 board structure is
enforced.

# Installation
There are no installation options for the script itself; just download
and guarantee you have a good python environment and you should be ready.

The only prerequisite is the [python image library](https://pypi.python.org/pypi/Pillow/),
which is avaiable via pip.  So, if you get some kind of library dependency
warning, just install via `pip install Pillow` and your environment should be set.


# Execution
Below are the standard help instructions from the program itself.

```
usage: composite.py [-h] [-d DIR_IMAGES] [-n GAME_NAME] [-c CARD_COUNT]
                    [-g GAME_COUNT] [-G GAME_FILE]
                    image_free

A simple script for generating bingo-style game boards

positional arguments:
  image_free            Absolute path to 'free' image for center board

optional arguments:
  -h, --help            show this help message and exit
  -d DIR_IMAGES, --dir_images DIR_IMAGES
                        Path for input images.
  -n GAME_NAME, --game_name GAME_NAME
                        Name for header row (e.g. 'bingo'), must match prefix
                        of image files
  -c CARD_COUNT, --card_count CARD_COUNT
                        How many card files should be generated?
  -g GAME_COUNT, --game_count GAME_COUNT
                        How many game listings should be generated?
  -G GAME_FILE, --game_file GAME_FILE
                        Destination for game file in text
```

## Example run
One set of images is provided in the [holiday](holiday) folder.

**NOTE: The images in this holiday directory are likely copyright and are not
valid for non-personal or commercial use.  The author of this package claims
no rights or guarantees for the usage of these sample images, which are provided
purely for example runs.**

Here are some genreated examples to enjoy.

![example games](holiday/example_games.txt)

![example card](holiday/example_card.jpg)

# Support
Support is not provided for this library, but you're welcome to ping the author.
Enjoy!
