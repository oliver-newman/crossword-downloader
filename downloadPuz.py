"""
Python script to be used with chron, to download the .puz version of the 
New York Times crossword every day and go back in time until the local
archive is up-to-date.
Oliver Newman: July 9, 2016
"""
from datetime import datetime, timedelta
from pytz import timezone
from subprocess import call
from time import sleep
import os.path
import socket

ARCHIVE_PATH = "/Users/Oliver/Desktop/crosswords/NYT_archive/"
URL_HEAD     = "http://www.nytimes.com/svc/crosswords/v2/puzzle/daily-"
EARLIEST_PUZ = {
  "day": 20,
  "month": 11,
  "year": 1993
}


"""
Returns True if internet is connected (Google responds), False otherwise
Source: http://stackoverflow.com/questions/20913411/test-if-an-internet-
  connection-is-present-in-python
"""
def internetOn():
  remoteServer = "www.google.com"

  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(remoteServer)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False


"""
Returns the date of the latest available crossword: the current day, unless
  1. After 10 PM EST, or
  2. After 7 PM EST on a Saturday or Sunday
"""
def latestAvailablePuzDate():
  today = datetime.now(timezone("America/New_York"))

  weekDay = today.weekday()
  hour    = today.hour

  # Download the next day's crossword, if available (after 7 PM on a weekend,
  # or after 10 PM on a weekday)
  nextPuzAvailable = (hour >= 22) or (weekDay > 4 and hour >= 19)
  if nextPuzAvailable:
    today += timedelta(days=1)
    
  return today


"""
Returns the URL of the .puz file for the inputted datetime
"""
def puzURL(today):
  # Date components
  day   = str(today.day).zfill(2)
  month = str(today.month).zfill(2)
  year  = str(today.year)

  fullURL = URL_HEAD + year + "-" + month + "-" + day + ".puz"

  return fullURL


"""
Returns a dict containing, for a given day's puzzle:
  yearPath:  full path for the year directory for the .puz to be downloaded
  monthPath: full path for the month directory for the .puz to be downloaded
  fileName:  full file name to which the .puz should be downloaded
"""
def filePath(today):
  # Date components
  day       = str(today.day).zfill(2)
  month     = str(today.month)
  monthName = today.strftime("%B")[:3] # First three letters of month name
  year      = str(today.year)

  # Construct desired file name
  yearDir   = ARCHIVE_PATH + year + "/"
  monthDir  = yearDir + month + "/"
  fileName  = monthDir + monthName + day + year[2:] + ".puz"

  filePathDict = {
    "yearPath" : yearDir, 
    "monthPath": monthDir,
    "fileName" : fileName
  }

  return filePathDict


"""
Returns True if puzDate matches day before earliest .puz available; False
otherwise
"""
def atEarliestPuz(puzDate):
  rightDay   = (puzDate.day == EARLIEST_PUZ["day"])
  rightMonth = (puzDate.month == EARLIEST_PUZ["month"])
  rightYear  = (puzDate.year  == EARLIEST_PUZ["year"])

  return (rightDay and rightMonth and rightYear)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
  # Checks internet connectivity every 5 min, until internet is connected
  while not internetOn():
    sleep(300)

  puzDate = latestAvailablePuzDate()
  upToDate = False

  while not upToDate:
    url = puzURL(puzDate)
    filePathDict = filePath(puzDate) # Dict containing components of file path

    # If all files have been downloaded up to today, end loop
    if os.path.exists(filePathDict["fileName"]) or atEarliestPuz(puzDate):
      upToDate = True
      continue

    # Check if destination directory exists; if not, construct the necessary
    # portions
    if not os.path.exists(filePathDict["monthPath"]):
      if not os.path.exists(filePathDict["yearPath"]):
        call(["mkdir", filePathDict["yearPath"]]) # Create year directory
      
      call(["mkdir", filePathDict["monthPath"]]) # Create month directory

    # Download the day's crossword to the desired location
    call(["curl", "-o", filePathDict["fileName"], url])

    # Adjust today variable to previous day to fully update archive
    puzDate = puzDate - timedelta(days=1)



