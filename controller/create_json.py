import json
import eyed3
import os


def createJsonData(
        track_folder: str = "",
        # Adding parameter for playlist, if any
        numOfPlaylists: int = 2,
        json_save_dir: str = ".\\",
        json_file_name: str = "test_sample.json"
):
    track_dir = os.path.join(track_folder)

    # Create song database from track folder
    songdb = []
    idx = 0
    for file in os.listdir(track_dir):
        trackURL = f"{track_dir}\\{file}"
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

    # Create playlist list
    playlist = []
    for idx in range(numOfPlaylists):
        songlist = [0, 1]
        name = "sad"
        count = len(songlist)
        playlist_data = {
            "name": name,
            "count": count,
            "songlist": songlist
        }
        playlist.append(playlist_data)

    username = "username"
    json_data = {
        "profile": username,
        "songdb": songdb,
        "play_list": playlist
    }

    with open(f'{json_save_dir}{json_file_name}', "w", encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)


if __name__ == '__main__':
    direct = 'C:\\Users\\Victus\\Downloads\\Music'

    createJsonData(
        track_folder=direct
    )
