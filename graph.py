import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap


class GraphResult(QObject):
    round_ended = pyqtSignal()
    experiment_ended = pyqtSignal(int)  # emits the users total

    def __init__(self, window, max_trials):
        super().__init__()
        self.window = window
        self.max_trials = max_trials

        self.sum = 0
        self.blackjack_threshold = 21
        self.trial_num = 0
        self.results_list = []  # the list of card values the participant has drawn
        self.trials_completed = []  # the list of trials completed

        self.min_x = 0  # will be used to determine the axes range
        self.min_y = 0
        self.max_x = 6
        self.max_y = 30

    def get_trial_num(self, card_results):
        self.trial_num = len(card_results)
        self.trials_completed.append(self.trial_num)

    def get_sum(self, card_results):
        self.sum = sum(card_results)
        self.results_list.append(self.sum)

    def show_sum(self):
        self.window.lbl_sum.setText(f"Your current sum is: {self.sum}")
        self.window.lbl_sum.show()

    def update_graph(self):
        x = self.trials_completed
        y = self.results_list
        plt.plot(x, y)
        plt.xlim(self.min_x, self.max_x)
        plt.ylim(self.min_y, self.max_y)
        plt.ylabel('Card Sum', fontsize=14)
        plt.xlabel('Number of Cards Drawn', fontsize=14)
        plt.axhspan(self.blackjack_threshold, 30, facecolor='red')
        plt.savefig('total_graph.png')

    def show_graph(self):  # update pixmap
        graph_pixmap = QPixmap("total_graph.png")
        self.window.lbl_graph.setPixmap(graph_pixmap)

    def end_round_or_expt(self):
        if max(self.trials_completed) == self.max_trials:
            self.experiment_ended.emit(self.sum)
        else:
            self.round_ended.emit()

    def plot(self, results):  # results is the selected card, it is emitted when chosen and connected to plot
        self.get_trial_num(results)
        self.get_sum(results)
        self.show_sum()
        self.update_graph()
        self.show_graph()
        self.end_round_or_expt()






