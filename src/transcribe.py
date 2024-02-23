from app import App
from services.TelegramService import TelegramService

def main():
    app = App()

    ok, msg = app.verify_env_variables()
    if not ok:
        exit(1)

    app.set_service(service=TelegramService())
    app.run()

if __name__ == "__main__":
    main()
