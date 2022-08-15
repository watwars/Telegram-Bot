# from dotenv import load_dotenv
from server import app

if __name__ == '__main__':
    app.run(host='localhost', port=8443, threaded=True)
