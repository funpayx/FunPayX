from fpx import FunPayTools


class FunPayManager:
    _instance: FunPayTools | None = None

    @classmethod
    def init(cls, gkey: str, gseal: str):
        cls._instance = FunPayTools(gkey=gkey, gseal=gseal)

    @classmethod
    def get(cls) -> FunPayTools:
        if cls._instance is None:
            raise RuntimeError("Аккаунт не инициализирован")
        return cls._instance