import glob
import os

import pytest

from chat_analyzer.analysis.analyzer import analyze
from chat_analyzer.models.app_data import AnalysisType, OutputFormat, AppArgs, AnalysisArgs
from chat_analyzer.parsing.parser import load
from chat_analyzer.test.utils import get_test_path
from chat_analyzer.visualization.visualizer import output

params = {
    "hour_interval": 1,
    "subject": "User One"
}


class TestApp():

    @pytest.mark.parametrize("out_format", [OutputFormat.JSON, OutputFormat.PLOT_PNG])
    def test_run_all_analyses(self, out_format):
        all_analysis = [AnalysisArgs(t, params) for t in AnalysisType]
        path = get_test_path("*.txt")
        args = AppArgs(path, get_test_path("."), out_format, all_analysis)

        chats = load(args)
        results = analyze(chats, args)
        assert results is not None

        output(results, args)

    @classmethod
    def teardown_class(cls):
        patterns = ["chat_simple_1_*.*", "chat_simple_2_*.*"]
        for pattern in patterns:
            for file in glob.glob(get_test_path(pattern)):
                os.remove(file)