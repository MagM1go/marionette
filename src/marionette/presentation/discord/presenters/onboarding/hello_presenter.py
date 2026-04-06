with open("assets/text") as file:
    text = file.read()


class HelloPresenter:
    @staticmethod
    def present() -> str:
        return text
