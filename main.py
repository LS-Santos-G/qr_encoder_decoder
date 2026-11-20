from views.main_menu import MainWindow


def main() -> None:
    app: MainWindow = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()