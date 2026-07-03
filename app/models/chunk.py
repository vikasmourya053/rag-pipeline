from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    metadata: dict