#takes about 40 ms
import os, time, shutil
from collections import namedtuple
from time import strftime

userpath = os.environ.get("USERPROFILE") #C:/Users/[person]

windowsSpotlightPath = userpath + r"\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets\\"
destPath = userpath + r"\Desktop\Spotlight_Images\Test\\"

if (not os.path.isdir(userpath + r"\Desktop\Spotlight_Images")):
	os.mkdir(userpath + r"\Desktop\Spotlight_Images")
	os.mkdir(userpath + r"\Desktop\Spotlight_Images\Test")
	with open(userpath + r"\Desktop\Spotlight_Images\Test\count.txt", "w+") as countFile:
		countFile.write("0")

spotlightImages = []
TimeRef = namedtuple("TimeRef","month day year")
olderThan = TimeRef(month=5,day=19,year=2018)
biggerThan = 1024*20
today = strftime("%m%d%Y",time.localtime()) #month,day,year


fileSize = lambda file: os.path.getsize(windowsSpotlightPath + file)
files = os.listdir(windowsSpotlightPath)

files.sort(reverse=True,key=fileSize)

def isSpotlightImage(file):
    absPath = windowsSpotlightPath + file
    metadata = os.stat(absPath)
    isBigger = metadata.st_size > biggerThan
    creationDate = time.localtime(metadata.st_ctime)
    isNewer = ((creationDate.tm_mon > olderThan.month) or \
              (creationDate.tm_mday > olderThan.day)) and \
              (creationDate.tm_year >= olderThan.year)
    if (isNewer and isBigger):
        return True
    else:
        return False

i = 0
while(isSpotlightImage(files[i])):
    spotlightImages.append(files[i])
    i += 1
del files

with open(os.path.join(destPath, "count.txt"),'r+') as imageCountFile:
    countStr = imageCountFile.read()
    for img in spotlightImages:
        countInt = int(countStr) + 1
        countStr = str(countInt)
        imageCountFile.seek(0)
        newName = today + "_" + countStr
        shutil.copy2(windowsSpotlightPath + img, destPath + newName + ".png")
        imageCountFile.truncate()
        imageCountFile.write(countStr)
