from can_frame import *


def main():
    try:
        frame=CanFrame(ID="10100", data="1")
    except Exception as e:
        print(e)
        return
    frame.convert()

    print(str(frame))

if __name__ == "__main__":
    main()