import chat_analyzer.args_helper as args_helper
import chat_analyzer.parsing.parser as parser
import chat_analyzer.analysis.analyzer as analyzer
import chat_analyzer.visualization.visualizer as visualizer


def run():
    args = args_helper.get_args()

    chats = parser.load(args)
    results = analyzer.analyze(chats, args)
    visualizer.output(results, args)

    print("All is done")
