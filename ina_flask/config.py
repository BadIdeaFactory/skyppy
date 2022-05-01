import yaml
from dataclasses import dataclass

with open("config.yaml") as file:
    configuration = yaml.safe_load(file)


@dataclass
class Option:
    server_url: str = "http://0.0.0.0:8080/"
    max_video_lenght_in_minutes: int = 15

    def __post_init__(self):
        if type(self.max_video_lenght_in_minutes) != int:
            raise ValueError("max_video_lenght_in_minutes must be integer")

        if type(self.server_url) != str:
            raise ValueError("server_url must be string")


option = Option(
    server_url=configuration["server_url"],
    max_video_lenght_in_minutes=configuration["max_video_lenght_in_minutes"],
)

if __name__ == "__main__":

    print(option.__dict__)
    print(option.max_video_lenght_in_minutes)
