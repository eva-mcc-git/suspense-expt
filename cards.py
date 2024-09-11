from random import randint
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Cards(QObject):
    cards_drawn = pyqtSignal()  # used to trigger suspense survey pop up
    selected_card_value = pyqtSignal(list)  # emits the card value needed to plot the sum

    def __init__(self, window, assigned_condition, trial, card_draws_per_condition, card_deck):
        super(Cards, self).__init__()
        self.window = window
        self.condition = assigned_condition
        self.trial = trial
        # the line below is a dictionary of dictionaries. The key is condition and in the sub-dictionary, the keys are trial
        # numbers and the values correspond to the cards that will be selected on each trial
        self.card_draws_per_condition = card_draws_per_condition
        self.card_deck = card_deck

        self.shuffle_timer = QTimer()
        self.shuffle_count = 0  # will use this to count shuffles
        self.max_shuffle_count = 10  # will use this to stop the shuffle at 10
        self.shuffle_distance = 60

        self.window.btn_start.clicked.connect(self.flip_cards)
        self.shuffle_timer.timeout.connect(self.shuffle_cards)

        self.card_colours = ['white', 'pink', 'red']

        self.card_results = []  # stores the card drawn on each trial
        self.trial_num = 0  # counts the trials

    def start_timer(self):
        self.shuffle_timer.start(125)

    def flip_cards(self):  # turn them face down
        self.window.lbl_next_round.hide()
        for card in self.window.wdg_cards.findChildren(QLabel):  # cards all in one widget to allow looping through each one
            card.setText("")
            card.setStyleSheet("background-color: grey; border: 2px solid black;")
        self.start_timer()  # start shuffle timer

    def unflip_cards(self):
        card_count = 0  # used as an index to grab numbers from the card deck list
        for card in self.window.wdg_cards.findChildren(QLabel):
            card_count += 1
            random_num = randint(0,2)
            colour = self.card_colours[random_num]  # randomly assign a colour from our colour list
            card.setText(self.card_deck[card_count - 1])  # assign a number to each card
            card.setStyleSheet(f"background-color: {colour}; border: 2px solid black;")

    def shuffle_cards(self):
        widget_width = self.window.wdg_cards.width()
        widget_height = self.window.wdg_cards.height()

        if self.shuffle_count < self.max_shuffle_count:  # shuffle counter
            self.shuffle_count += 1
            for card in self.window.wdg_cards.findChildren(QLabel):
                # random value to add to current x, y co-ords
                random_x = randint(-self.shuffle_distance, self.shuffle_distance)  # a random number from -60 to +60
                random_y = randint(-self.shuffle_distance, self.shuffle_distance)

                new_x = card.x() + random_x  # taking the existing x and y and adding the random numbers generated above
                new_y = card.y() + random_y
                # the next step is to keep the cards within the 4 boundaries of the widgets they are in
                if (
                        new_x > 0 and  # left boundary
                        new_x + card.width() < widget_width and  # right boundary
                        new_y > 0 and  # top boundary
                        new_y + card.height() < widget_height  # bottom boundary
                ):
                    card.move(new_x, new_y)
        else:  # i.e., if shuffle limit is hit
            self.shuffle_timer.stop()
            self.select_two_cards()
            self.shuffle_count = 0  # resetting this for the next round

    def select_two_cards(self):
        self.get_trial_num()  # updates trial_num used in next line
        # the next line gets the two cards to be displayed after user has shuffled
        selected_cards = self.card_draws_per_condition[self.condition][f"Trial {self.trial_num}"]
        # selected cards is a list with 2 values
        self.window.lbl_card_result1.setText(selected_cards[0])
        self.window.lbl_card_result2.setText(selected_cards[1])
        self.window.lbl_card_result1.show()
        self.window.lbl_card_result2.show()

        self.cards_drawn.emit()  # connects to ask_suspense method in suspense recorder
        self.unflip_cards()  # turn cards face up

    def get_trial_num(self):
        if not self.card_results:
            self.trial_num = 1
        else:
            self.trial_num = len(self.card_results) + 1
    def record_card_num(self, result):
        if result == "colour":  # if the lottery wheel lands on colour this corresponds to the top of the 2 cards
            card_number = self.window.lbl_card_result2.text()
        else:  # white corresponds to the bottom of the 2
            card_number = self.window.lbl_card_result1.text()
        self.card_results.append(int(card_number))
        self.selected_card_value.emit(self.card_results)  # connects to plot in Graph class




