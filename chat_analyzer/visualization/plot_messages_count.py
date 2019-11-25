import matplotlib.pyplot as plt

from chat_analyzer.analysis.chat_messages_count import ChatMessageStat


def plot_messages_per_user_count(stats: ChatMessageStat):
    fig, plots = plt.subplots(1, 3)

    sorted_mess = sorted(stats.user_stats, key=lambda stat: stat.message_count)[:5]
    sorted_word = sorted(stats.user_stats, key=lambda stat: stat.word_count)[:5]
    sorted_avg = sorted(stats.user_stats, key=lambda stat: stat.avg_words_per_message)[:5]

    message_count = [user.message_count for user in sorted_mess]
    word_count = [user.word_count for user in sorted_word]
    avg_words_per_message = [user.avg_words_per_message for user in sorted_avg]

    names = [user.username for user in sorted_mess]
    bars = plots[0].bar(names, message_count)
    plots[0].set_title("Message Count")
    auto_label(bars, plots[0])

    names = [user.username for user in sorted_word]
    bars = plots[1].bar(names, word_count)
    plots[1].set_title("Word Count")
    auto_label(bars, plots[1])

    names = [user.username for user in sorted_avg]
    bars = plots[2].bar(names, avg_words_per_message)
    plots[2].set_title("Avg. words per msg")
    auto_label(bars, plots[2])

    fig.suptitle('Message Count Stats')
    plt.show()


def auto_label(bars, plots):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in bars:
        height = bar.get_height()
        plots.annotate('{}'.format(height),
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom')
