from dataclasses import dataclass
from enum import Enum, auto

import yaml

with open("config.yaml") as file:
    configuration = yaml.safe_load(file)


class deploy_option(Enum):
    LOCAL_MACHINE = auto()
    WEB = auto()


@dataclass
class Option:
    server_url: str = "http://0.0.0.0:8080/"
    max_video_lenght_in_minutes: int = 15
    deploy: str = ""
    db_url: str = ""

    def __post_init__(self):
        if type(self.max_video_lenght_in_minutes) != int:
            raise ValueError("max_video_lenght_in_minutes must be integer")

        if type(self.server_url) != str:
            raise ValueError("server_url must be string")

        if deploy_option.LOCAL_MACHINE.name == self.deploy:
            self.db_url = "sqlite:///status.db"

        if deploy_option.WEB.name == self.deploy:
            import web_deploy

            self.db_url = web_deploy.sqlUrl


option = Option(
    server_url=configuration["server_url"],
    max_video_lenght_in_minutes=configuration["max_video_lenght_in_minutes"],
    deploy=configuration["deploy"],
)

if __name__ == "__main__":

    print(option.__dict__)
    print(option.max_video_lenght_in_minutes)
    print(option.deploy)
    print(option.db_url)
