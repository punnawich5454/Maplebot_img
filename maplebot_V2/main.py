from gui import create_app


def main():
    app, window = create_app()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
