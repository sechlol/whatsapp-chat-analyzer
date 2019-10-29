import numpy as np
import matplotlib.pyplot as plt

from analysis.chat_time_stats import StatsWrapper


def plot_messages_per_day_count(wrapper: StatsWrapper):
    sorted_dates = wrapper.get_sorted_dates()
    indexed_raw = wrapper.get_indexed_by_date_raw()
    cumulative = [0] * len(sorted_dates)

    for sender in wrapper.legend:
        sender_y = [indexed_raw[x].get(sender, 0) for x in sorted_dates]
        plt.bar(sorted_dates, sender_y, bottom=cumulative)
        cumulative = np.add(cumulative, sender_y)

    plt.legend(wrapper.legend)
    plt.show()

def plot_initiation_score_per_day(wrapper: StatsWrapper):
    sorted_dates = wrapper.get_sorted_dates()
    indexed_raw = wrapper.get_indexed_by_date_raw()

    for sender in wrapper.legend:
        sender_y = [indexed_raw[x].get(sender, 0) for x in sorted_dates]
        plt.plot(sorted_dates, sender_y)

    plt.legend(wrapper.legend)
    plt.show()