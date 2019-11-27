from typing import List

from chat_analyzer.analysis.chat_messages_count import messages_per_user_count
from chat_analyzer.analysis.chat_time_stats import messages_per_day_count, initiation_score_per_interval, \
    chat_engagement
from chat_analyzer.analysis.words_finder import get_top_used_words
from chat_analyzer.models.app_data import AppArgs, AnalysisType, AnalysisResult
from chat_analyzer.models.chat_data import Chat


def analyze(chats: List[Chat], args: AppArgs) -> List[AnalysisResult]:
    results = []
    for analysis in args.analyses:
        for chat in chats:

            if analysis.type == AnalysisType.MESSAGES_COUNT:
                result = messages_per_user_count(chat=chat)
            elif analysis.type == AnalysisType.MESSAGES_PER_DAY:
                result = messages_per_day_count(chat=chat)
            elif analysis.type == AnalysisType.WORDS_MOST_USED:
                result = get_top_used_words(chat=chat, **analysis.optional_par)
            elif analysis.type == AnalysisType.INITIATION_SCORES:
                result = initiation_score_per_interval(chat=chat, **analysis.optional_par)
            else:
                result = None

            if result:
                results.append(AnalysisResult(data=result, args=analysis, name=chat.name))

        if analysis.type == AnalysisType.ENGAGEMENT_SCORE:
            results.append(
                AnalysisResult(
                    data=chat_engagement(chats=chats, **analysis.optional_par),
                    args=analysis,
                    name="_".join([chat.name for chat in chats]).replace(" ", "_")
                ))

    return results
