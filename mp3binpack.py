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
totalSecsAllSongs = 0.0
mp3z = {}
for filename in filenames:
    if not filename.endswith(".mp3"):
        continue
#   print(filename.replace(".mp3", ""))
    audio = MP3(filename)
#   print("\t{}".format(audio.info.length))
    totalSecsAllSongs += audio.info.length
    mp3z[filename] = audio.info.length

print("TotalSecs = {} seconds or {}".format(totalSecsAllSongs, datetime.timedelta(seconds = totalSecsAllSongs)))

bins = binpacking.to_constant_bin_number(mp3z, 4)
# print("===== dict\n",mp3z,"\n",bins)

# b = list(mp3z.values())
bins = binpacking.to_constant_volume(mp3z, max_cd_time)
# print("\n\n===== list\n",b,"\n",bins)

print("\n\nResult - max cd time {} seconds".format(max_cd_time))
for i, songsInCd in enumerate(bins):
    totalCdTime = sum(songsInCd.values())
    # getting time in mins:seconds instead of just seconds. The int strips out the milliseconds
    songsInCd = {x: str(datetime.timedelta(seconds = int(songsInCd[x]))) for x in songsInCd}
    print("CD {} - {} songs - {} seconds {}\n\n".format(
        i, len(songsInCd.keys()), datetime.timedelta(seconds = totalCdTime), json.dumps(songsInCd, indent=4)))
    if isMovingFiles is None:
        continue
    newdirname = "{:02d}".format(i)
    if not os.path.isdir(newdirname):
        os.mkdir(newdirname)
    for mp3 in songsInCd.keys():
        print("Moving {}".format(mp3))
        shutil.move("{}".format(mp3), "{}/{}".format(newdirname, mp3))
