import numpy as np


class Track:
    def __init__(
            self,
            name: str = "Unknown",
            artist: str = "Unknown",
            duration: int = 0,
            image_url: str = ""
    ) -> None:
        self.name = name
        self.artist = artist
        self.duration = duration
        self.image_url = image_url

    def getTrackName(self) -> str:
        return self.name

    def getArtistName(self) -> str:
        return self.artist

    def getTrackDuration(self) -> int:
        return self.duration

    def setImageURL(self, URL: str = "") -> None:
        self.image_url = URL


class PlayBack:
    def __init__(
            self,
            playBackList: "list[Track]",
            name: str = "Unknown",
            artist: str = "Unknown",
            image_url: str = ""
    ) -> None:
        self.name = name
        self.artist = artist
        self.image_url = image_url
        self.playBackList = playBackList
        self.currTrackIndex = 0

    def getTrackAtIndex(self, index: int = 0):
        self.currTrackIndex = index
        return self.playBackList[index]

    def addTrack(self, newTrack: Track) -> None:
        self.playBackList.append(newTrack)


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
            playBack: PlayBack = None,
            position: int = 0
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

        if playBack is None:
            self.playBack = []
        else:
            self.playBack = playBack

    def toggleShuffleMode(self) -> None:
        self.isShuffle = not self.isShuffle
        # TODO: Convert to shuffle mode

    def toggleRepeatMode(self) -> None:
        if self.repeatMode == 0:
            self.isRepeat = True
            self.repeatMode += 1
            # TODO: Repeat mode for all track in playlist

        elif self.repeatMode == 1:
            self.repeatMode += 1
            # TODO: Repeat mode for only current track

        else:
            self.isRepeat = False
            self.repeatMode = 0
            # TODO: Don't repeat track when the playback is done

    def toggleMuteMode(self) -> None:
        if not self.isMute:
            self.systemVolume = 0
            self.isMute = True
            # TODO: Set the system volume by alssaudio
        else:
            self.isMute = False
            self.systemVolume = self.currVolume
            # TODO: Set the system volume by alssaudio

    def togglePlayPause(self) -> None:
        if not self.isPlaying:
            self.isPlaying = True
            # TODO: Play music
        else:
            self.isPlaying = False
            # TODO: Pause music

    def setCurrVolume(self, currVolume: int) -> None:
        self.currVolume = currVolume
        # TODO: Using alssaudio to set system volume


if __name__ == '__main__':

    mp = MusicPlayer()
