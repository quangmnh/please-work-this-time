# import numpy as np
import os

from pygame import mixer
from copy import deepcopy
import random
import eyed3
import json
import pandas as pd


class Track:
    def __init__(
            self,
            trackId: int = 0,
            trackURL: str = "",
            imageURL: str = ""
    ) -> None:
        self.trackId = trackId
        self.trackURL = trackURL
        audio = eyed3.load(trackURL)
        self.name = audio.tag.title
        self.artist = audio.tag.artist
        self.duration = audio.info.time_secs
        self.imageURL = imageURL

    '''------------ DEFINE GETTER FUNCTIONS ----------'''
    def getTrackName(self) -> str:
        return self.name

    def getArtistName(self) -> str:
        return self.artist

    def getTrackDuration(self) -> int:
        return int(self.duration)

    def getTrackURL(self) -> str:
        return self.trackURL

    '''------------- DEFINE SETTER FUNCTIONS ----------'''
    def setImageURL(self, imageURL: str = "") -> None:
        self.imageURL = imageURL


class TrackDatabase:
    def __init__(
            self,
            trackList: "list[Track]" = []
    ) -> None:
        self.trackList = trackList
        self.numOfTracks = 0

    def addTrack(
            self,
            newTrack: Track
    ) -> None:
        self.trackList.append(newTrack)
        self.numOfTracks += 1

    def getTrackAtIndex(
            self,
            index: int = 0
    ) -> "any":
        if len(self.trackList) == 0:
            return None
        else:
            return self.trackList[index]

    def displayTrackDBInfo(self) -> None:
        for i in range(len(self.trackList)):
            print(
                f'Duration: {self.trackList[i].getTrackDuration()},\n'
                f'Artist: {self.trackList[i].getArtistName()},\n'
                f'Track name: {self.trackList[i].getTrackName()},\n'
                f'Track URL: {self.trackList[i].getTrackURL()},\n'
                f'-----------------------------------\n')


class PlayList:
    def __init__(
            self,
            _trackDB: TrackDatabase,
            id_list: "list[int]",
            name: str = "Unknown",
    ) -> None:
        self.playListName = name
        self.numOfTracks = len(id_list)
        self.trackList = []

        for idx in id_list:
            self.trackList.append(_trackDB.getTrackAtIndex(idx))

    def addTrack(
            self,
            newTrack: Track
    ) -> None:
        self.trackList.append(newTrack)
        self.numOfTracks += 1

    def getTrackAtIndex(
            self,
            index: int = 0
    ) -> "any":
        if len(self.trackList) == 0:
            return None
        else:
            return self.trackList[index]

    def printPlaylistInfo(self) -> None:
        print(
            f'Playlist name: {self.playListName},\n'
            f'Number of Tracks: {self.numOfTracks},\n'
            f'-----------------------------------\n')

        for i in range(len(self.trackList)):
            print(
                f'Duration: {self.trackList[i].getTrackDuration()},\n'
                f'Artist: {self.trackList[i].getArtistName()},\n'
                f'Track name: {self.trackList[i].getTrackName()},\n'
                f'Track URL: {self.trackList[i].getTrackURL()},\n'
                f'-----------------------------------\n')


class MusicPlayer:
    def __init__(
            self,
            playBack: "list[Track]" = [],
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
        self.playBack = playBack
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
        self.player.music.load(self.playBack[index].getTrackURL())
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


def getDBFromJSON(json_dir: str) -> TrackDatabase:
    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        trackDB = TrackDatabase()
        for track_info in data['songdb']:
            track = Track(
                track_info.get("id"),
                track_info.get("url")
            )
            if track is not None:
                trackDB.addTrack(track)

    return trackDB


def getPlaylistList(
        json_dir: str,
        trackDB: TrackDatabase
) -> "list[PlayList]":

    playlistList = []

    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        for playlist_info in data['play_list']:
            playlist = PlayList(
                _trackDB=trackDB,
                name=playlist_info.get("name"),
                id_list=playlist_info.get("songlist")
            )
            playlist.printPlaylistInfo()

            if playlist is not None:
                playlistList.append(playlist)

    return playlistList


if __name__ == '__main__':
    '''
        Sửa lại chỗ này thành os.path.join(os.getcwd() + '/sample.json') khi chạy ở main.py (nếu có)
        Code ở dưới chỉ dùng để test trong file MusicPlayer.py
    '''
    json_dir = os.path.join('./../sample.json')
    trackDB = getDBFromJSON(json_dir)
    playlistList = getPlaylistList(
        json_dir,
        trackDB
    )

    trackDB.displayTrackDBInfo()

    for playlist in playlistList:
        playlist.printPlaylistInfo()



