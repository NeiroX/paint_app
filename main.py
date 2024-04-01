from GUI.application_gui import ApplicationGUI


def main() -> None:
    """
    Run 'python main.py' to run the application.
    Application functionality are defined in README file.
    :return: None
    """
    app = ApplicationGUI()
    app.run()


if __name__ == "__main__":
    main()
