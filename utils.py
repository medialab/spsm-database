import os
from datetime import date

class FileNaming:
    def __init__(self, title, dir="", ext="csv"):
        self.title = title
        self.dir = dir
        self.ext = ext
        self.todays_date = self.derive_name()

    def derive_name(self):
        today_basename = f"{self.title}_{date.today()}"
        i = 1
        while os.path.isfile(os.path.join(self.dir, f"{today_basename}_{i}.{self.ext}")):
            i+=1
        return os.path.join(self.dir, f"{today_basename}_{i}.{self.ext}")
