from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cards import *
from lottery_wheel import *
from graph import *
from ui import *
from suspense_recorder import *
from user_inputs_validator import *
from experiment import *
from results import *

app = QApplication([])
window = uic.loadUi("assignment3.ui")
window.stacked_widget.setCurrentIndex(0)


# --------- Experiment Setup --------------------------
results_file = "ExperimentResults.csv"
max_trials = 5
card_deck = ["6", "1", "9", "3", "4", "0", "7", "2", "3"]
conditions = ["high suspense", "low suspense"]

cards_drawn_high_suspense = {"Trial 1": ['3', '3'],
                             "Trial 2": ['8', '5'],
                             "Trial 3": ['4', '2'],
                             "Trial 4": ['0', '2'],
                             "Trial 5": ['6', '3']}
cards_drawn_low_suspense = {"Trial 1": ['3', '3'],
                            "Trial 2": ['1', '2'],
                            "Trial 3": ['4', '7'],
                            "Trial 4": ['7', '6'],
                            "Trial 5": ['4', '1']}

# By creating a dictionary of dictionaries I can later easily access the cards that need to be drawn
# per trial for the participant's condition
card_draws_per_condition = {'high suspense': cards_drawn_high_suspense,
                            'low suspense': cards_drawn_low_suspense}

experiment = Experiment(results_file, conditions)
experiment.run_experiment_setup()


# ---------- Ui Setup -----------------------
ui = Ui(window)
ui.run_ui_setup()


# ---------- User Inputs: Consent & Demog Info ------------

participant_inputs = UserInputsValidator(window)

participant_inputs.consent_given.connect(ui.update_consent)  # updates a boolean attribute in the Ui class
participant_inputs.valid_user_inputs.connect(ui.update_valid_inputs)  # also updates boolean attribute in Ui class
# below will check the above attributes are true before changing the page, i.e., we have received consent & demog info
window.btn_next.clicked.connect(ui.page_change_checks)

# ------------------ The Game ----------------------------------

# --------------- Instantiate Relevant CLasses -----------------
suspense = SuspenseRecorder(window, max_trials)  # manages suspense survey

cards = Cards(window,
              experiment.assigned_condition,
              participant_inputs.trial_num,
              card_draws_per_condition,
              card_deck)  # manages anything related to the card deck

spin_wheel = LotteryWheel(window)  # manages the lottery wheel

display = GraphResult(window, max_trials)  # manages the graph

results = Results(results_file, experiment.assigned_condition)  # used to record condition, demog info & suspense results to a file

# ----------------- Connect Signals To Slots -------------------------------

# takes the validated inputs emitted by this signal and updates the relevant attribute in results class
participant_inputs.valid_user_inputs.connect(results.update_demog_info)

# connect the signal that cards have been draw to a slot that asks user for their self-report of suspense
cards.cards_drawn.connect(suspense.ask_suspense)

# connects the keyboard press event "c" with the wheel spin
suspense.my_widget.keyPressed.connect(spin_wheel.start_timer)
suspense.my_widget.keyReleased.connect(spin_wheel.stop_timer)

# gets the value of the chosen card
spin_wheel.lottery_result.connect(cards.record_card_num)

# takes the card value emitted by this signal, calculates the sum and plots
cards.selected_card_value.connect(display.plot)

# either loops the game or ends it if the max trials has been reached
display.round_ended.connect(ui.trial_reset)
display.experiment_ended.connect(ui.end_game)

# when all trials are complete, the results are store in an attribute in the results class
suspense.suspense_inputs_complete.connect(results.update_suspense)

# once the experiment is over, record the results
display.experiment_ended.connect(results.record_results)

#  ---------- Show Ui ------------------------------

window.show()
app.exec()

