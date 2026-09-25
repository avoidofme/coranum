import sys


def main() -> None:
    print("Hellow orld")


if __name__ == "__main__":
    try:
        main()
    finally:
        print("exiting...")
        sys.exit(0)
