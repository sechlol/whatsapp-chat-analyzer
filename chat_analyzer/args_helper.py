import argparse
import os
from typing import List, Optional

from chat_analyzer.models.app_data import AnalysisArgs, AppArgs, AnalysisType, OutputFormat

allowed_formats = {
    "json": OutputFormat.JSON,
    "png": OutputFormat.PLOT_PNG,
    "plot": OutputFormat.PLOT_UI,
}

arg_parser = argparse.ArgumentParser(description='WhatsApp chat analyzer')
arg_parser.add_argument("path",
                        type=str,
                        help="The path for the chat file(s) to analyze. Supports wildcards.")
arg_parser.add_argument("--chat_stats",
                        default=argparse.SUPPRESS,
                        action="store_true",
                        help="Simple stats on messages and words count")
arg_parser.add_argument("--messages_day",
                        default=argparse.SUPPRESS,
                        action="store_true",
                        help="Messages per day per person")
arg_parser.add_argument("--initiation",
                        action="store",
                        type=int,
                        default=argparse.SUPPRESS,
                        metavar="interval",
                        help="Who initiates the conversation more often. Must specify [interval]")
arg_parser.add_argument("--engagement",
                        action="store",
                        type=str,
                        default=argparse.SUPPRESS,
                        metavar="subject",
                        help="Shows the engagement of one person (subject) with other partecipants over time. Must specify [subject: str]")
arg_parser.add_argument("--word_rank",
                        nargs=2,
                        type=int,
                        default=argparse.SUPPRESS,
                        metavar=("limit", "min_size"),
                        help="Most used words. May specify parameters [limit=10, min_size=4]")
arg_parser.add_argument("--format",
                        action="store",
                        default=argparse.SUPPRESS,
                        metavar="format",
                        choices=allowed_formats.keys(),
                        type=str,
                        help=f"Output mode. accepted values are: [{','.join(allowed_formats.keys())}]")
arg_parser.add_argument("--out",
                        action="store",
                        default=argparse.SUPPRESS,
                        metavar="out_path",
                        type=str,
                        help="By default is the same folder as input.")


def get_args(manual_args: Optional[List[str]] = None) -> AppArgs:
    analysis_list = []
    parsed_args = vars(arg_parser.parse_args(manual_args))

    path = parsed_args["path"]
    dir_path = os.path.dirname(path)

    if not os.path.exists(dir_path):
        raise Exception(f"Input path {dir_path} does not exist.")

    initiation = parsed_args.get("initiation")
    engagement = parsed_args.get("engagement")
    word_rank = parsed_args.get("word_rank")
    out_format = allowed_formats.get(parsed_args.get("format"), OutputFormat.JSON)
    out_path = parsed_args.get("out", dir_path)

    if not os.path.exists(out_path):
        raise Exception(f"Output path {out_path} does not exist.")

    # Parameters for analysis
    if "chat_stats" in parsed_args:
        analysis_list.append(AnalysisArgs(AnalysisType.MESSAGES_COUNT))
    if "messages_day" in parsed_args:
        analysis_list.append(AnalysisArgs(AnalysisType.MESSAGES_PER_DAY))
    if initiation:
        analysis_list.append(
            AnalysisArgs(
                AnalysisType.INITIATION_SCORES,
                {"hour_interval": initiation},
            ))
    if engagement:
        analysis_list.append(
            AnalysisArgs(
                AnalysisType.ENGAGEMENT_SCORE,
                {"subject": engagement},
            ))
    if word_rank:
        analysis_list.append(
            AnalysisArgs(
                AnalysisType.WORDS_MOST_USED,
                {"limit": word_rank[0], "min_size": word_rank[1]}
            ))

    if not analysis_list:
        raise Exception("Must select at least one analysis type")

    return AppArgs(
        in_files_path=path,
        out_path=out_path,
        analyses=analysis_list,
        out_format=out_format,
    )
