import numpy as np
import matplotlib.pyplot as plt

from chat_analyzer.analysis.chat_time_stats import StatsWrapper


def plot_messages_per_day_count(wrapper: StatsWrapper):
    sorted_dates = wrapper.get_sorted_dates()
    indexed_raw = wrapper.get_indexed_by_date_raw()
    cumulative = [0] * len(sorted_dates)

    for sender in wrapper.legend:
        sender_y = [indexed_raw[x].get(sender, 0) for x in sorted_dates]
        plt.bar(sorted_dates, sender_y, bottom=cumulative)
        cumulative = np.add(cumulative, sender_y)

    plt.legend(wrapper.legend)
    return plt


def plot_initiation_score_per_day(wrapper: StatsWrapper):
    sorted_dates = wrapper.get_sorted_dates()
    indexed_raw = wrapper.get_indexed_by_date_raw()

    for sender in wrapper.legend:
        sender_y = [indexed_raw[x].get(sender, 0) for x in sorted_dates]
        plt.plot(sorted_dates, sender_y)

    plt.legend(wrapper.legend)
    return plt

def plot_engagement(wrapper: StatsWrapper):
    legend = wrapper.legend

    x_dates = [stat.date_sent for stat in wrapper.stats]
    y_vals = []

    for label in legend:
        y_vals.append([stat.get_indexed_values().get(label, 0) for stat in wrapper.stats])

    plt.stackplot(x_dates, y_vals)
    plt.legend(wrapper.legend, loc='upper left')

    return plt
