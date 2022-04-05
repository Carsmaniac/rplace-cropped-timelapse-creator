import cv2
import os
import shutil
from PIL import Image

print("\n\nMake sure you've met the requirements on the GitHub page, this script won't check everything's okay, and will crash if anything is wrong :)\n")

print("Type a name then press enter")
suffix = input("Timelapse name: ")

print("\nEnter co-ords with a comma in between, and no spaces or brackets, like this: 150,1097")
print("")
top_left = input("Top left co-ords: ").split(",")
bottom_right = input("Bottom right co-ords: ").split(",")
for i in range(2):
    top_left[i] = int(top_left[i])
    bottom_right[i] = int(bottom_right[i]) + 1

print("\nSpeed determines how many frames are put in the video, e.g. a speed of 3 means every 3rd frame is included")
print("rplace.space took screenshots every 30 minutes, so I'd recommend a speed of 3 or 4")
speed = int(input("Speed (whole number, no decimals): "))

scale = 2

if top_left[0] < 1000 && top_left[1] < 1000:
    start_index = 0 # 1k x 1k canvas
elif top_left[0] >= 1000 && top_left[1] < 1000:
    start_index = 3022 # 2k x 1k canvas
else:
    start_index = 7193 # 2k x 2k canvas


print("Cropping images")

if os.path.exists("cropped_{}".format(suffix)):
    shutil.rmtree("cropped_{}".format(suffix))
os.mkdir("cropped_{}".format(suffix))

total = len(os.listdir())
counter = 1

for image_file in os.listdir()[start_index:]:
    if counter % speed == 0:
        if image_file[-3:] == "png":
            with Image.open(image_file) as img:
                img = img.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
                img = img.resize((img.size[0] * scale, img.size[1] * scale), Image.NEAREST)
                img.save("cropped_{}/{}".format(suffix, image_file), "PNG")
        print("{}/{} ({})".format(counter, total - start_index, suffix))
    counter += 1

print("Making video file")

if os.path.exists("output_{}".format(suffix)):
    shutil.rmtree("output_{}".format(suffix))
os.mkdir("output_{}".format(suffix))

frame_array = []
for image_file in sorted(os.listdir("cropped_{}".format(suffix))):
    if image_file[-3:] == "png":
        img = cv2.imread("cropped_{}/".format(suffix) + image_file)
        height, width, layers = img.shape
        size = (width, height)
        frame_array.append(img)

video_output = cv2.VideoWriter("output_{}/video.avi".format(suffix), cv2.VideoWriter_fourcc(*'DIVX'), 30.0, size)

for frame in frame_array:
    video_output.write(frame)
video_output.release()

print("Converting to mp4")

os.system("ffmpeg -i output_{}/video.avi \"output_{}/Timelapse_{}.mp4\"".format(suffix, suffix, suffix))

shutil.rmtree("cropped_{}".format(suffix))
os.remove("output_{}/video.avi".format(suffix))
