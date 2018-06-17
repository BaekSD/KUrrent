from PeerPack import gui, app
import threading

if __name__ == "__main__":
    try:
        gui.show()
        app.exec_()
        gui.clearFocus()
        gui_th = threading.Thread(target=gui.update_torrent_list)
        gui_th.daemon = True
        gui_th.start()
    except RuntimeError:
        pass