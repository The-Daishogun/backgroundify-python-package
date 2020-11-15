import requests
import os
import datetime
from pathlib import Path


def main():
    url = get_img_url()
    path = save_file(url)
    change_background(path)


# returns the url of image of the day
def get_img_url(description=False):
    # the bing URL
    bing = "https://www.bing.com"
    # URL of the JSON info of the Bing Picture of the day
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    json = requests.get(url).json()
    # gets image description
    img_desc = json["images"][0]["copyright"]
    # get the image URL from the JSON file
    img_url = bing + json["images"][0]["url"]

    if description:
        return img_url, img_desc
    else:
        return img_url


# saves the image and returns the path of saved image
def save_file(url):
    # create the path string
    filename = str(datetime.date.today()) + ".jpg"
    save_path = str(Path.home()) + "/Pictures/PythonBingWallpaper/"
    # concatnating them for simplicity
    path = save_path + filename
    # download the image and converting it to bytes
    image = requests.get(url).content
    # creates a dir for storing images and passes if the dir already exists
    try:
        os.mkdir(save_path)
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

