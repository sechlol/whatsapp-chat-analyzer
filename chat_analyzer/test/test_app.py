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

    @pytest.mark.parametrize("out_format", [OutputFormat.PLOT_PNG])
    def test_all_analysis_json(self, out_format):
        all_analysis = [AnalysisArgs(t, params) for t in AnalysisType]
        path = get_test_path("*.txt")
        args = AppArgs(path, get_test_path("."), out_format, all_analysis)

        chats = load(args)
        results = analyze(chats, args)
        assert results is not None

        output(results, args)

    def test_supported_analysis_plot(self):
        all_analysis = [
            AnalysisType.MESSAGES_PER_DAY,
            AnalysisType.MESSAGES_COUNT,
            AnalysisType.INITIATION_SCORES,
            AnalysisType.ENGAGEMENT_SCORE,
        ]
        output_format = OutputFormat.PLOT_PNG
        path = get_test_path("*.txt")

        chats = load(path)
        for t in all_analysis:
            data = analyze(t, chats, **params)
            assert data is not None

            output(output_format, t, data)
