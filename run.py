# Do not use app.run_server here
# Instead, simply import the 'app' object from your 'main' module
from main import app

if __name__ == '__main__':
    app.run_server(port=8060)
