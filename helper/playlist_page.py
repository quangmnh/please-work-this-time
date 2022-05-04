from PyQt5 import QtWidgets

from views.ui_main import Ui_MainWindow
from views.pages import PlaylistPage
from views.components import PlaylistLabel

from utils1.display_list_item import display_list_item
from utils1.snake_case import snake_case

# EXAMPLE FUNCTION


def playlist_play():
    pass


def playlist_song_play():
    pass
# END :EXAMPLE FUNCTION


def create_playlist_dialog(parent: QtWidgets.QWidget, page_widget: QtWidgets.QStackedWidget, playlist_list_widget: QtWidgets.QListWidget):

    dialog = QtWidgets.QInputDialog(parent)
    dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
    dialog.setWindowTitle("Create Playlist")
    dialog.setLabelText('Playlist Name:')
    dialog.setStyleSheet("color: white; background-color: rgb(50,50,50);")
    ok = dialog.exec_()
    playlist_name = dialog.textValue()

    if (ok and playlist_name):
        add_playlist_page(page_widget, playlist_name, playlist_list_widget)


def add_playlist_page(page_widget: QtWidgets.QStackedWidget, playlist_name: str, playlist_list_widget: QtWidgets.QListWidget):
    """Add playlist page to page stack widget

    Args:
        page_widget (QtWidgets.QStackedWidget): Stack widget to add page to.
        playlist_name (str): Name of playlist to add.
        playlist_list_widget (QtWidgets.QListWidget): List widget to display all playlists.
    """
    playlist_label = PlaylistLabel(
        playlist_name, lambda: change_playlist_page(page_widget, playlist_name))

    # Add label to list widget
    entry = QtWidgets.QListWidgetItem(playlist_list_widget)
    playlist_list_widget.addItem(entry)
    entry.setSizeHint(playlist_label.minimumSizeHint())
    playlist_list_widget.setItemWidget(entry, playlist_label)

    playlist_page = PlaylistPage(playlist_name, playlist_song_play, playlist_play,
                                 lambda: remove_playlist_page(page_widget, playlist_name, playlist_list_widget, entry))
    # Add page to page stack
    page_widget.addWidget(playlist_page)


def change_playlist_page(page_widget: QtWidgets.QStackedWidget, playlist_name: str):
    num_page = page_widget.count()
    for i in range(num_page):
        w = page_widget.widget(i)
        if (hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name)):
            page_widget.setCurrentIndex(i)
            break


def remove_playlist_page(page_widget: QtWidgets.QStackedWidget, playlist_name: str, playlist_list_widget: QtWidgets.QListWidget, playlist_label: QtWidgets.QListWidgetItem):
    num_page = page_widget.count()
    for i in range(num_page):
        w = page_widget.widget(i)
        if (hasattr(w, "playlist_name") and w.playlist_name == snake_case(playlist_name)):
            page_widget.removeWidget(w)
            page_widget.setCurrentIndex(0)
            break

    # Remove label from list widget
    playlist_list_widget.takeItem(playlist_list_widget.row(playlist_label))
