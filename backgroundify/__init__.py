import requests
import os
import datetime
from pathlib import Path


def main():
    url = get_img_url()
    path = save_file(url, str(Path.home()) + "/Pictures/PythonBingWallpaper/")
    change_background(path)


# returns the url of image of the day
def get_img_url(description=False, day=1):
    # the bing URL
    bing = "https://www.bing.com"
    # URL of the JSON info of the Bing Picture of the day
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={}&mkt=en-US".format(
        day
    )
    json = requests.get(url).json()
    # gets image description
    img_desc = json["images"][day - 1]["copyright"]
    # get the image URL from the JSON file
    img_url = bing + json["images"][day - 1]["url"]
    if description:
        return img_url, img_desc
    else:
        return img_url


# Changes the file name to YY-MM-DD.jpg and returns the name
def get_filename():
    return str(datetime.date.today()) + ".jpg"


# saves the image and returns the path of saved image
def save_file(url, path, filename):
    # concatnating them for simplicity
    path = path + filename
    # download the image and converting it to bytes
    image = requests.get(url).content
    # creates a dir for storing images and passes if the dir already exists
    try:
        os.mkdir("pic")
    except FileExistsError as f:
        pass
    # creates a file in binary mode and writes image bytes to file
    f = open(path, "wb")
    f.write(image)
    f.close()
    return path


# changes the system background
def change_background(filepath):
    os.system(
        "gsettings set org.gnome.desktop.background picture-uri file:////{}".format(
            filepath
        )
    )


if __name__ == "__main__":
    main()

