from pathlib import Path

# TODO: над будет придумать способ попадать в корень получше, иначе это не очень гибко
_ASSETS_DIR = Path(__file__).resolve().parents[6] / "assets"

with open(f"{_ASSETS_DIR}/text/hello.txt") as file:
    _text = file.read()


class HelloPresenter:
    @staticmethod
    def present() -> str:
        return _text
