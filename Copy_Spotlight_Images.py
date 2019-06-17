#81.05 ms on average of 100 trials (calculated by powershell)
#About 2ms when the main action of this script is run and all the setup is done (after line 45)
import os, time, shutil
import shelve #used as a way for persistent storage. Creates a .dat file that acts like a dictionary
from time import strftime #format a string with time specific formatters
begin = time.perf_counter()

userpath = os.environ.get("USERPROFILE") #C:/Users/[person]

windowsSpotlightPath = userpath + r"\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets\\"
destPath = userpath + r"\Desktop\Spotlight_Images\Test\\"

if (not os.path.isdir(userpath + r"\Desktop\Spotlight_Images")):
	os.mkdir(userpath + r"\Desktop\Spotlight_Images")
	os.mkdir(userpath + r"\Desktop\Spotlight_Images\Test")
	

os.chdir(destPath)
spotlightImages = []
biggerThan = 1024*200 #bigger than 200KB
today = strftime("%m%d%Y",time.localtime()) #month,day,year


fileSize = lambda file: os.path.getsize(windowsSpotlightPath + file)
files = os.listdir(windowsSpotlightPath)

files.sort(reverse=True,key=fileSize)

def isSpotlightImage(file):
    absPath = windowsSpotlightPath + file
    metadata = os.stat(absPath)
    isBigger = metadata.st_size > biggerThan
    if (isBigger):
        return True
    else:
        return False

i = 0
while(i < len(files) and isSpotlightImage(files[i])): #short-circuit so we don't get an index out of bounds (if all files were valid spotlight images)
    spotlightImages.append(files[i])
    i += 1
del files

countFile = shelve.open("count")
count = 0

try:
	count = countFile["count"]
except KeyError:
	countFile["count"] = 0

for img in spotlightImages:
	count += 1
	newName = today + "_" + str(count)
	shutil.copy2(windowsSpotlightPath + img, destPath + newName + ".png")

countFile["count"] = count