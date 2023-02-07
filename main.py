import uvicorn
from dotenv import load_dotenv

from src.app import app

load_dotenv()
DEVELOPMENT = True


def main():
    if DEVELOPMENT:
        uvicorn.run('src.app:app', host="localhost", port=8000, reload=True, ssl_keyfile="./localhost-key.pem",
                    ssl_certfile="./localhost.pem")
    else:
        uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
