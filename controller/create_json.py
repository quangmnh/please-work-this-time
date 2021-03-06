# -*- coding: utf-8 -*-

import json
import eyed3
import os


def createJsonData(
        track_folder: str,
        # Adding parameter for playlist, if any
        numOfPlaylists: int = 5,
        json_save_dir: str = os.path.join(os.getcwd()),
        json_file_name: str = "sample_windows.json"
):
    track_dir = os.path.join(track_folder)

    # Create song database from track folder
    songdb = []
    idx = 0
    for file in os.listdir(track_dir):
        trackURL = os.path.join(track_dir, file)
        audio = eyed3.load(trackURL)
        print(f'{audio.tag.title}\n'
              f'{audio.tag.artist}\n'
              f'{audio.info.time_secs}'
              f'--------------------\n')
        track_data = {
            "id": idx,
            "name": audio.tag.title,
            "artist": audio.tag.artist,
            "duration": int(audio.info.time_secs),
            "image_url": "https://sakjdlsadjsa.com",
            "url": trackURL
        }
        songdb.append(track_data)
        idx += 1

    # Create playlist list
    playlist = []
    for idx in range(numOfPlaylists):
        songlist = [0, 1]
        name = "sad"
        count = len(songlist)
        playlist_data = {
            "id": idx,
            "name": name,
            "count": count,
            "songlist": songlist
        }
        playlist.append(playlist_data)

    username = "username"
    json_data = {
        "profile": username,
        "songdb": songdb,
        "play_list": playlist,
        "angry_playlist": 0,
        "happy_playlist": 1,
        "neutral_playlist": 2,
        "sad_playlist": 3,
        "surprise_playlist": 4
    }

    with open(f'{json_save_dir}{json_file_name}', "w", encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)


def updateTrackDatabaseFromFolderToJsonFile(
        track_folder: str,
        json_dir: str
):
    track_dir = os.path.join(track_folder)
    songdb = []
    idx = 0
    for file in os.listdir(track_dir):
        trackURL = os.path.join(track_dir, file)
        audio = eyed3.load(trackURL)
        print(f'{audio.tag.title}\n'
              f'{audio.tag.artist}\n'
              f'{audio.info.time_secs}'
              f'--------------------\n')
        track_data = {
            "id": idx,
            "name": audio.tag.title,
            "artist": audio.tag.artist,
            "duration": int(audio.info.time_secs),
            "image_url": "https://sakjdlsadjsa.com",
            "url": trackURL
        }
        songdb.append(track_data)
        idx += 1

    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        data['songdb'] = songdb

    with open(json_dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def updateEmotionPlaylistJson(
        json_dir: str,
        emotion: str,
        playlistIndex: int = 0
):
    with open(json_dir, encoding='utf-8') as f:
        data = json.load(f)

        if emotion == 'angry':
            data['angry_playlist'] = playlistIndex
        elif emotion == 'happy':
            data['happy_playlist'] = playlistIndex
        elif emotion == 'neutral':
            data['neutral_playlist'] = playlistIndex
        elif emotion == 'sad':
            data['sad_playlist'] = playlistIndex
        else:
            data['surprise_playlist'] = playlistIndex

    with open(json_dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    direct = os.path.join('C:/', 'Users', 'Victus', 'Downloads', 'Music')

    createJsonData(
        track_folder=direct,
        json_save_dir='./../'
    )
