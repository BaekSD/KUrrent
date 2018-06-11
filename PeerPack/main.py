from PeerPack import p, app

if __name__ == "__main__":
    try:
        p.show()
        app.exec_()
        p.clearFocus()
    except RuntimeError:
        pass