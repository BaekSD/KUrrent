from TrackerPack.app import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, use_reloader=False, port=5000)