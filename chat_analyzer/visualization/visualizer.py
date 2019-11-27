import json
import logging
from typing import List

from chat_analyzer.models.app_data import AnalysisType, OutputFormat, AnalysisResult, AppArgs
from chat_analyzer.visualization.plot_messages_count import plot_messages_per_user_count
from chat_analyzer.visualization.plot_rank import plot_words_rank
from chat_analyzer.visualization.plot_time_serie import plot_messages_per_day_count, plot_initiation_score_per_day

logger = logging.getLogger(__name__)


def output(results_list: List[AnalysisResult], args: AppArgs):
    if args.out_format == OutputFormat.JSON:
        for result in results_list:
            _write_json(result, args.out_path)

    else:
        _plot(results_list, args)


def _plot(results_list: List[AnalysisResult], args: AppArgs):
    function_map = {
        AnalysisType.MESSAGES_COUNT: plot_messages_per_user_count,
        AnalysisType.INITIATION_SCORES: plot_initiation_score_per_day,
        AnalysisType.ENGAGEMENT_SCORE: plot_initiation_score_per_day,
        AnalysisType.MESSAGES_PER_DAY: plot_messages_per_day_count,
        AnalysisType.WORDS_MOST_USED: plot_words_rank,
    }

    for result in results_list:
        plotting_function = function_map.get(result.args.type)
        if not plotting_function:
            logger.warning(f"Plotting for analysis mode {result.args.type.name} is not supported. Fallback to JSON")
            _write_json(result, args.out_path)
            continue

        plot = plotting_function(result.data)

        if args.out_format == OutputFormat.PLOT_UI:
            plot.show()
        elif args.out_format == OutputFormat.PLOT_PNG:
            plot.savefig(f"{args.out_path}/{result.name}_{result.args.type.name}.png")

        # Must clear the plot or it will overlap with the next one
        plot.clf()


def _write_json(result: AnalysisResult, out_path: str):
    json_data = _to_json_recursive(result.data)
    with open(f"{out_path}/{result.name}_{result.args.type.name}.json", 'w') as f:
        json.dump(json_data, f)


def _to_json_recursive(data):
    # if object has a to_json method, call it and return the result
    to_json_method = getattr(data, "to_json", None)
    if callable(to_json_method):
        return to_json_method()

    # if data is a list, recursively go through each element
    if isinstance(data, list):
        return [_to_json_recursive(d) for d in data]

    return data
