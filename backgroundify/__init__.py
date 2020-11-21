import requests
import os
from datetime import date, timedelta


class Backgroundify(object):
    def __init__(self, days=1):
        """a class that help you get the Bing image of the day

        Args:
            days (int, optional): Shows how many days you want to go back. Defaults to 1. Max = 8
        """
        self.days = days if days <= 8 else 8
        self.bing = "https://www.bing.com"
        self.reqURL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={}&mkt=en-US".format(
            self.days
        )
        self.imgs = {}

    def get_imgs(self):
        """returns an object. each entry is an object containing title, copyright info, url, and filename of a bing picture

        Returns:
            Object: each entry is an object containing title, copyright info, url, and filename of a bing picture
        """
        response = requests.get(self.reqURL).json()
        for i, img in enumerate(response["images"]):
            file_name = str(date.today() - timedelta(days=i))
            self.imgs[i] = {
                "title": img["title"],
                "copyright": img["copyright"],
                "url": self.bing + img["url"],
                "filename": file_name,
                "ext": ".jpg",
            }
        return self.imgs

    def save_files(self):
        """saves the files to /static/pic/ folder. 
        """
        try:
            os.mkdir("static")
            os.mkdir("static/pic")
        except FileExistsError as f:
            pass
        for i in self.imgs:
            path = "static/pic/" + self.imgs[i]["filename"] + self.imgs[i]["ext"]
            if os.path.exists(path):
                pass
            else:
                image = requests.get(self.imgs[i]["url"]).content
                f = open(path, "wb")
                f.write(image)
                f.close()

    def change_wallpaper(self):
        filepath = os.path.join(os.getcwd(), "static/pic/", self.imgs[0]["filename"])
        os.system(
            "gsettings set org.gnome.desktop.background picture-uri file:////{}".format(
                filepath
            )
        )
