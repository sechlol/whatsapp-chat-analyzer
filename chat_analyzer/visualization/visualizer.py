import json
from enum import Enum
from typing import List

from chat_analyzer.analysis.analyzer import AnalysisType
from chat_analyzer.analysis.chat_messages_count import ChatMessageStat
from chat_analyzer.analysis.chat_time_stats import StatsWrapper
from chat_analyzer.visualization.plot_messages_count import plot_messages_per_user_count
from chat_analyzer.visualization.plot_time_serie import plot_messages_per_day_count, plot_initiation_score_per_day


class OutputFormat(Enum):
    JSON = 1
    CHART_UI = 2
    CHART_IMG = 3


def output(out_mode: OutputFormat, analysis: AnalysisType, data_list: List):
    if out_mode == OutputFormat.JSON:
        _write_json(data_list)
        return

    if not isinstance(data_list, list):
        data_list = [data_list]

    _plot(out_mode, analysis, data_list)


def _plot(out_mode: OutputFormat, analysis: AnalysisType, data_list):
    for index, data in enumerate(data_list):
        if isinstance(data, ChatMessageStat):
            plot = plot_messages_per_user_count(data)
        elif isinstance(data, StatsWrapper):
            if analysis == AnalysisType.INITIATION_SCORES or analysis == AnalysisType.ENGAGEMENT_SCORE:
                plot = plot_initiation_score_per_day(data)
            elif analysis == AnalysisType.MESSAGES_PER_DAY:
                plot = plot_messages_per_day_count(data)
            else:
                raise Exception(f"Plotting for analysis mode {analysis.name} is not supported")
        else:
            raise Exception(f"Plotting of data type {type(data)} is not supported")

        if out_mode == OutputFormat.CHART_UI:
            plot.show()
        elif out_mode == OutputFormat.CHART_IMG:
            filename = f"chat_plot_{index}.png"
            plot.savefig(filename)
        plot.clf()


def _write_json(data):
    json_data = _to_json_recursive(data)
    with open("chat_data.json", 'w') as f:
        json.dump(json_data, f)

def _to_json_recursive(data):
    if isinstance(data, list):
        return [_to_json_recursive(d) for d in data]

    if isinstance(data, ChatMessageStat) or isinstance(data, StatsWrapper):
        return data.to_json()

    return data
