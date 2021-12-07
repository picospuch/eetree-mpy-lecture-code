from buzzer_music import music
from time import sleep
from my_people_my_country import song

mymusic = music(song)

while True:
    print(mymusic.tick())
    sleep(0.04)
