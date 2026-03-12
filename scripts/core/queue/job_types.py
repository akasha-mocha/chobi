from dataclasses import dataclass
from typing import Dict


@dataclass
class Job:

    id: str
    type: str
    priority: int
    payload: Dict

    status: str = "queued"