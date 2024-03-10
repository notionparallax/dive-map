# %%
from PIL import Image, ExifTags
from datetime import datetime
import os

# %%

img = Image.open("dive_photos/GOPR0098.JPG")
img_exif = img.getexif()
print(type(img_exif))
# <class 'PIL.Image.Exif'>

if img_exif is None:
    print("Sorry, image has no exif data.")
else:
    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            print(f"📸 {ExifTags.TAGS[key]}:{val} ({key})")
        else:
            print(f"{key}:{val}")
# %%
print(
    ExifTags.TAGS[306],
    f"-{img_exif[306]}-",
    datetime.strptime(img_exif[306], "%Y:%m:%d %H:%M:%S"),
)


# %%
photos = []
for f in os.listdir("dive_photos"):
    img = Image.open(f"dive_photos/{f}")
    img_exif = img.getexif()
    dt = datetime.strptime(img_exif[306], "%Y:%m:%d %H:%M:%S")
    photos.append(
        {
            "filename": f,
            "datetime": dt,
            "marker_type": "",
            "marker_number": "",
        }
    )
photos
# %%
