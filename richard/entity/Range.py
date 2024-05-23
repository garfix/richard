from dataclasses import dataclass


@dataclass(frozen=True)
class Range:
    entity: str
    ids: list[str]


    def __iter__(self):
        for id in self.ids:
            yield id

    def __len__(self) -> int:
        return len(self.ids)