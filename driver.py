import multiprocessing

from app.app import App


def main():
    multiprocessing.freeze_support()
    app = App()
    app.run()


if __name__ == '__main__':
    main()
