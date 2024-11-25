from base import app

if __name__ == '__main__':
    app.run(port=4263, debug=True, threaded=True,  use_reloader=False)