"""Entry point — interactive loop until the user types 'quit'."""

from agent import run

QUIT_SIGNALS = {"quit", "exit", "q"}


def prompt_country() -> str:
    """Ask repeatedly until the user types a non-empty country name."""
    while True:
        country = input("Country (or 'quit' to exit): ").strip()
        if country:
            return country
        print("Please enter a country name.")


def main() -> None:
    print("=== Biggest Cities Agent ===")

    while True:
        country = prompt_country()

        if country.lower() in QUIT_SIGNALS:
            print("Bye!")
            break

        print()
        print(run(country))  # pass country directly — no query string needed
        print()


if __name__ == "__main__":
    main()
