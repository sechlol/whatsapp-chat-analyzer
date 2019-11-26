from chat_analyzer.analysis.analyzer import AnalysisType
import chat_analyzer.parsing.parser as parser
import chat_analyzer.analysis.analyzer as analyzer
import chat_analyzer.visualization.visualizer as visualizer


def run():
    file_name_pattern = "S:\Projects\git\whatsapp-chat-analyzer\\tt\*.txt"
    analysis_type = AnalysisType.WORDS_MOST_USED
    output_type = visualizer.OutputFormat.JSON
    params = {
       # "subject": "Christian",
        #"hour_interval": 8
    }

    chats = parser.load(file_name_pattern)
    data = analyzer.analyze(analysis_type, chats, **params)
    result = visualizer.output(output_type, analysis_type, data)

    if result:
        print("All is done")
