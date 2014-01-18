"""The GUI for making GUIs."""

from wxwrapper.views import MainFrame

def main():
    frame = MainFrame()
    frame.run()

if __name__ == "__main__":
    main()