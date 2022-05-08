from controller.MusicPlayer import Track, TrackDatabase
import os
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent


def convert_from_songDB_to_list_dict(trackDB: TrackDatabase) -> "list[dict]":
    track_list = []
    index = 0
    for track in trackDB.getTrackList():
        track_data = {
            "id": index,
            "name": track.getTrackName(),
            "artist_name": track.getArtistName(),
            "track_url": track.getTrackURL()
        }
        track_list.append(track_data)
        index += 1

    return track_list


def convert_from_track_list_to_list_dict(track_lists: "list[Track]") -> "list[dict]":
    index = 0
    track_list = []
    for track in track_lists:
        track_data = {
            "id": index,
            "name": track.getTrackName(),
            "artist_name": track.getArtistName(),
            "track_url": track.getTrackURL()
        }
        track_list.append(track_data)
        index += 1

    return track_list


def load_soundtrack_playlist(song_library: "list[dict]") -> QMediaPlaylist:
    soundtrack_playlist = QMediaPlaylist()
    soundtrack_playlist.setPlaybackMode(QMediaPlaylist.Loop)

    for song in song_library:
        track_url = song.get("url")
        media = QMediaContent(track_url)
        soundtrack_playlist.addMedia(media)

    return soundtrack_playlist
