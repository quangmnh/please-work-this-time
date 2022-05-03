from PyQt5 import QtWidgets


def display_list_item(list_widget: QtWidgets.QListWidget, list_of_items):
    """Display list of items in a list widget.

    Args:
        list_widget (QtWidgets.QListWidget): The list widget object to display items in.
        list_of_items (array): list of custom widgets instances to display.
    """
    # Dunno if this should be called but it's here for now to prevent adding items on every call.
    list_widget.clear()

    for item in list_of_items:
        entry = QtWidgets.QListWidgetItem(list_widget)
        list_widget.addItem(entry)
        entry.setSizeHint(item.minimumSizeHint())
        list_widget.setItemWidget(entry, item)
