from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Item:
    id: Optional[int]
    name: str


@dataclass
class Machine:
    id: Optional[int]
    name: str


@dataclass
class Recipe:
    id: Optional[int]
    item: Item
    output_amount: int
    machine: Machine
    inputs: Dict[Item, int]
