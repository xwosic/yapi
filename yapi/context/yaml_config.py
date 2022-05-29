import yaml


class Yamloader:
    def __init__(self, path: str) -> None:
        with open(path) as f:
            self.content: dict = yaml.load(f, Loader=yaml.Loader)

    def __getitem__(self, key: str):
        return self.content.get(key)
