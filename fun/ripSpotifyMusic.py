# credit to http://bartsimons.me/ripping-spotify-songs-on-macos/

# recordsong.py - record a song on Spotify with the help of Piezo

# Example usage:
#
# python3 recordsong.py spotify:track:21cp8L9Pei4AgysZVihjSv

import subprocess, sys, os, time, shutil, eyed3
from urllib.request import urlopen

# Setup variables
piezoStorageLocation = '/Users/jayden/Music/Piezo/'
ripStorageLocation   = '/Users/jayden/Music/Ripped/'

# Clear all previous recordings if they exist
for f in os.listdir(piezoStorageLocation):
    os.remove(os.path.join(piezoStorageLocation,f))

# Tell Spotify to pause, tell Piezo to record, tell Spotify to play a specified song
subprocess.Popen('osascript -e "tell application \\"Spotify\\" to pause"', shell=True, stdout=subprocess.PIPE).stdout.read()
time.sleep(.300)
subprocess.Popen('osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()
subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "play track \\"'+sys.argv[1]+'\\"" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()

time.sleep(1)

# Get the artist name, track name, album name and album artwork URL from Spotify
artist  = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artist" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
track   = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s name" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
album   = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s album" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
artwork = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artwork url" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')

# Download album artwork
artworkData = urlopen(artwork).read()

# Check every 500 milliseconds if Spotify has stopped playing
while subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "player state" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read() == b"playing\n":
    time.sleep(.500)

# Spotify has stopped playing, stop the recording in Piezo
subprocess.Popen('osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()


time.sleep(.500)

# Create directory for the artist
if not os.path.exists(ripStorageLocation+artist):
    os.makedirs(ripStorageLocation+artist)

# Create directory for the album
if not os.path.exists(ripStorageLocation+artist+"/"+album):
    os.makedirs(ripStorageLocation+artist+"/"+album)

# Move MP3 file from Piezo folder to the folder containing rips.
for f in os.listdir(piezoStorageLocation):
        if f.endswith(".mp3"):
            shutil.move(piezoStorageLocation+f, ripStorageLocation+artist+"/"+album+"/"+track+".mp3")

# Set and/or update ID3 information
musicFile = eyed3.load(ripStorageLocation+artist+"/"+album+"/"+track+".mp3")
musicFile.tag.images.set(3, artworkData, "image/jpeg", sys.argv[1])
musicFile.tag.artist = artist
musicFile.tag.album  = album
musicFile.tag.title  = track

musicFile.tag.save()

subprocess.Popen('osascript -e "quit app \\"Piezo\\""', shell=True, stdout=subprocess.PIPE).stdout.read()