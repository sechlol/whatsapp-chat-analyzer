from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np


def plot_words_rank(data: List[Tuple[str, int]]):
    labels = [item[0] for item in data]
    rank = [item[1] for item in data]
    y_pos = np.arange(len(labels))

    plt.bar(labels, rank, align='center')
    plt.xticks(y_pos, labels)
    plt.ylabel('Occurrence')
    plt.title('Most used words')

    return plt
