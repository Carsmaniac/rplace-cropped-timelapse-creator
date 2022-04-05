# r/Place Cropped Timelapse Creator

Creates timelapses of small areas on the r/Place 2022 canvas, like this

## Prerequisites

- OpenCV - `pip install opencv-python`
- Pillow - `pip install pillow`
- [ffmpeg](https://ffmpeg.org/) - Needs to be added to the system path, or `ffmpeg.exe` needs to be in the same folder as the `.py` file

## Usage

1. Download the collection of r/Place snapshots from [rplace.space](https://rplace.space/combined/), there is a text file with a link to a zip file in the `images` folder
2. Extract all PNGs to the `images` folder
3. Run `generate-timelapse.py` and follow the prompts

Your folder structure should look like this:
```
images
 ┃ 1648822500.png
 ┃ 1648822512.png
 ┃ 1648822759.png
 ┃ ...
 ┗ Where to get images.txt
ffmpeg.exe (or in system path)
generate-timelapse.py
```
