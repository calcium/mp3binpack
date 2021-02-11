import os
from mutagen.mp3 import MP3
import datetime
import binpacking
import json
import shutil

isMovingFiles = os.environ.get("movemp3")

# https://stackoverflow.com/questions/11680174/what-is-the-algorithm-to-optimally-fill-a-dvd-for-burning

max_cd_time = 4764
filenames = next(os.walk("./", topdown=True))[2]
totalSecs = 0.0
mp3z = {}
for filename in filenames:
    if not filename.endswith(".mp3"):
        continue
    audio = MP3(filename)
#   print(filename.replace(".mp3", ""))
#   print("\t{}".format(audio.info.length))
    totalSecs += audio.info.length
    mp3z[filename] = audio.info.length

print("TotalSecs = {} seconds or {}".format(totalSecs, datetime.timedelta(seconds = totalSecs)))

bins = binpacking.to_constant_bin_number(mp3z, 4)
#rint("===== dict\n",mp3z,"\n",bins)

b = list(mp3z.values())
bins = binpacking.to_constant_volume(mp3z, max_cd_time)
#rint("\n\n===== list\n",b,"\n",bins)

print("\n\nResult - max cd time {} seconds".format(max_cd_time))
for i, j in enumerate(bins):
    total = sum(j.values())
    print("CD {} - {} seconds {}\n\n".format(i, datetime.timedelta(seconds = total), json.dumps(j, indent=4)))
    if isMovingFiles is None:
        continue
    newdirname = "{:02d}".format(i)
    if not os.path.isdir(newdirname):
        os.mkdir(newdirname)
    for mp3 in j.keys():
        print("Moving {}".format(mp3))
        shutil.move("{}".format(mp3), "{}/{}".format(newdirname, mp3))
