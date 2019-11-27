import pytest

from chat_analyzer.args_helper import get_args
from chat_analyzer.models.app_data import AnalysisType, OutputFormat


class TestArgsHelper:
    exception_input = [
        "./file.txt",
        "./not_exist/file.txt",
        "./file.txt --out ./not_exist/",
    ]

    def test_accepts_multiple_words_subject(self):
        name = "Name Surname"
        args_input = f"./file.txt --engagement {name}"
        args = get_args(args_input.split())
        assert args.analyses[0].optional_par["subject"] == name

    def test_accepts_min_parameters(self):
        args_input = "./file.txt --chat_stats"
        args = get_args(args_input.split())

        assert args.out_path == "."
        assert args.in_files_path == "./file.txt"
        assert args.out_format == OutputFormat.JSON

        assert len(args.analyses) == 1
        analysis = args.analyses[0]
        assert analysis.type == AnalysisType.MESSAGES_COUNT
        assert not analysis.optional_par

    def test_accepts_all_parameters(self):
        args_input = "./file.txt --chat_stats --messages_day --initiation 1 --engagement aaa --word_rank 3 4 --format png --out ."
        args = get_args(args_input.split())

        assert args.out_path == "."
        assert args.in_files_path == "./file.txt"
        assert args.out_format == OutputFormat.PLOT_PNG

        assert len(args.analyses) == 5

        assert args.analyses[0].type == AnalysisType.MESSAGES_COUNT
        assert args.analyses[1].type == AnalysisType.MESSAGES_PER_DAY
        assert args.analyses[2].type == AnalysisType.INITIATION_SCORES
        assert args.analyses[3].type == AnalysisType.ENGAGEMENT_SCORE
        assert args.analyses[4].type == AnalysisType.WORDS_MOST_USED

        assert not args.analyses[0].optional_par
        assert not args.analyses[1].optional_par
        assert args.analyses[2].optional_par["hour_interval"] == 1
        assert args.analyses[3].optional_par["subject"] == "aaa"
        assert args.analyses[4].optional_par["limit"] == 3
        assert args.analyses[4].optional_par["min_size"] == 4

    @pytest.mark.parametrize("args_input", exception_input)
    def test_args_raise_exception(self, args_input):
        with pytest.raises(Exception):
            get_args(args_input.split())
