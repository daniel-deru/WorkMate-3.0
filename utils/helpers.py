# clears the window so it can be repainted
def clear_window(container):
    # This is to remove the previous widgets that were painted so the widgets don't get added twice
    prevItems = container.count()
    # check if there are widgets
    if prevItems > 0:
        for i in range(container.count()):
            item = container.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                container.removeItem(item.spacerItem())