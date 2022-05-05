# import numpy as np
from pygame import mixer
from copy import deepcopy
import random
import eyed3


class Track:
    def __init__(
            self,
            url
    ) -> None:
        self.url = url
        audio = eyed3.load(url)
        self.name = audio.tag.title
        self.artist = audio.tag.artist
        self.duration = audio.tag.duration
        self.image_url = ""
        # need to test this module for accessing id3 tag, might fail/ wrong usage

    def getTrackName(self) -> str:
        return self.name

    def getArtistName(self) -> str:
        return self.artist

    def getTrackDuration(self) -> int:
        return self.duration

    def setImageURL(self, URL: str = "") -> None:
        self.image_url = URL

    def getURL(self):
        return self.url


class MusicPlayer:
    def __init__(
            self,
            systemVolume: int = 0,
            isPlaying: bool = False,
            isShuffle: bool = False,
            isRepeat: bool = False,
            repeatMode: int = 0,
            isMute: bool = False,
            currVolume: int = 0,
            name: str = "Unknown",
            artist: str = "Unknown",
            position: int = 0,
    ) -> None:
        self.systemVolume = systemVolume
        self.isPlaying = isPlaying
        self.isShuffle = isShuffle
        self.isRepeat = isRepeat
        self.repeatMode = repeatMode
        self.isMute = isMute
        self.currVolume = currVolume
        self.name = name
        self.artist = artist
        self.position = position
        self.playBack = []
        self.playback_count = 0
        self.curr_playing = 0
        self.shuffle_pb = deepcopy(self.playBack)
        self.player = mixer

    def toggleShuffleMode(self) -> None:
        self.isShuffle = not self.isShuffle

    def addSong(self, track: Track):
        self.playBack.append(track)

    def toggleRepeatMode(self) -> None:
        self.isRepeat = not self.isRepeat

    def playSongAt(self, index):
        self.player.music.load(self.playBack[index].getURL())
        self.player.music.play()
        # To Do: change the player's ui

    def toggleMuteMode(self) -> None:
        self.isMute = not self.isMute

    def togglePlayPause(self) -> None:
        if self.isCurrPlaying():
            self.player.music.pause()
        else:
            self.player.music.unpause()

    def setCurrVolume(self, currVolume: int) -> None:
        self.currVolume = currVolume
        self.player.set_volume(currVolume)

    def getCurrPos(self):
        return self.player.get_pos()

    def setCurrVolume(self, currVolume: int) -> None:
        # self.currVolume = currVolume
        return self.player.get_volume(currVolume)

    def isCurrPlaying(self):
        return self.player.get_busy()

    def next(self):
        if self.isShuffle:
            self.curr_playing = random.randint(0, self.playback_count - 1)
        else:
            self.curr_playing = (self.curr_playing + 1) % self.playback_count
        self.playSongAt(self.curr_playing)
        # timer in the main decide when to next

    def prev(self):
        if self.isShuffle:
            self.curr_playing = random.randint(0, self.playback_count - 1)
        else:
            if self.curr_playing > 0:
                self.curr_playing = (self.curr_playing - 1)
            else:
                self.curr_playing = self.playback_count - 1
        self.playSongAt(self.curr_playing)


if __name__ == '__main__':
    mp = MusicPlayer()
