from chat_analyzer.analysis.analyzer import AnalysisType, analyze
from chat_analyzer.parsing.parser import load
from chat_analyzer.test.utils import get_test_path
from chat_analyzer.visualization.visualizer import OutputFormat, output

params = {
    "hour_interval": 1,
    "subject": "User One"
}


class TestApp():
    def test_all_analysis_json(self):
        all_analysis = [t for t in AnalysisType]
        output_format = OutputFormat.JSON
        path = get_test_path("*.txt")

        chats = load(path)
        for t in all_analysis:
            data = analyze(t, chats, **params)
            assert data is not None

            output(output_format, t, data)

    def test_supported_analysis_plot(self):
        all_analysis = [
            AnalysisType.MESSAGES_PER_DAY,
            AnalysisType.MESSAGES_COUNT,
            AnalysisType.INITIATION_SCORES,
            AnalysisType.ENGAGEMENT_SCORE,
        ]
        output_format = OutputFormat.CHART_IMG
        path = get_test_path("*.txt")

        chats = load(path)
        for t in all_analysis:
            data = analyze(t, chats, **params)
            assert data is not None

            output(output_format, t, data)
