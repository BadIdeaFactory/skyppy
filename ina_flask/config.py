from dataclasses import dataclass


@dataclass
class Option:
    server_url: dict


option = Option(server_url="http://0.0.0.0:8080/")

if __name__ == "__main__":

    print(option.__dict__)
