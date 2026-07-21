import uvicorn

from core.app import app
from core.settings import settings


def main():
    uvicorn.run(app=app, host=settings.DOMAIN, port=settings.PORT)


if __name__ == "__main__":
    main()
