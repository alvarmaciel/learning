from dataclasses import dataclass


@dataclass
class Laptop:
    machine_name: str = "DULL"

    def install_os(self) -> None:
        print("Installing OS")

    def format_hd(self) -> None:
        print("Formatting the hard drive")

    def create_admin_user(self, password: str) -> None:
        print(f"Creating admin user with password {password}.")


def reset_to_factory(laptop: Laptop, admin_passwd: str = "admin"):
    laptop.format_hd()
    if not laptop.machine_name == "DULL":
        raise Exception("Not DULL machine name")
    laptop.install_os()
    laptop.create_admin_user(admin_passwd)


def main() -> None:
    laptop = Laptop()
    print(laptop)
    reset_to_factory(laptop)


if __name__ == "__main__":
    main()
