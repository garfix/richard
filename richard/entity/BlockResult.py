from dataclasses import dataclass


@dataclass(frozen=True)
class BlockResult:

    products: list[any]
    error_code: str
    error_args: list[str]


    def successful(self):
        return self.error_code == "" and len(self.products) > 0
    

