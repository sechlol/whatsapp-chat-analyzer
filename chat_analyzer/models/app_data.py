from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class AnalysisType(Enum):
    MESSAGES_COUNT = 1
    MESSAGES_PER_DAY = 2
    WORDS_MOST_USED = 3
    INITIATION_SCORES = 4
    ENGAGEMENT_SCORE = 5


class OutputFormat(Enum):
    JSON = 1
    PLOT_UI = 2
    PLOT_PNG = 3


@dataclass()
class AnalysisArgs:
    type: AnalysisType
    optional_par: Dict = field(default_factory=dict)


@dataclass
class AppArgs:
    in_files_path: str
    out_path: str
    out_format: OutputFormat
    analyses: List[AnalysisArgs]


@dataclass
class AnalysisResult:
    name: str
    data: Any
    args: AnalysisArgs
