"""Entry point — interactive loop until the user types 'quit'."""

from agent import run

QUIT_SIGNALS = {"quit", "exit", "q"}


def prompt_country() -> str:
    """Ask repeatedly until the user types a non-empty country name.

    Java equivalent:
        String country = "";
        do { country = scanner.nextLine().strip(); } while (country.isEmpty());
    """
    while True:
        country = input("Country (or 'quit' to exit): ").strip()
        if country:
            return country
        print("Please enter a country name.")


def main() -> None:
    print("=== Biggest Cities Agent ===")

    # Loop until the user types a quit signal — like a do-while in Java.
    while True:
        country = prompt_country()

        if country.lower() in QUIT_SIGNALS:
            print("Bye!")
            break

        print()
        print(run(f"What are the three biggest cities in {country}?"))
        print()


if __name__ == "__main__":
    main()
