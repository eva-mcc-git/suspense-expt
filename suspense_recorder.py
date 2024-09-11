from lottery_wheel import KeyboardWidget
from ui import *


class SuspenseRecorder(QObject):
    suspense_inputs_complete = pyqtSignal(list)

    def __init__(self, window, max_trials):
        super().__init__()
        self.window = window
        self.max_trials = max_trials

        self.suspense = ""  #  will be updated with the user input
        self.min_suspense = 1  # the suspense scale is from 1 to 5
        self.max_suspense = 5
        self.suspense_inputs = []  # this will store the participant's self-reported feelings of suspense
        self.window.txt_suspense.textChanged.connect(self.verify_suspense_input)

        self.instructions_timer = QTimer()  # instructions for the lottery wheel to be given after suspense has been recorded
        self.instructions_delay = 800
        self.ui = Ui(self.window)  # creating an instance of the Ui class to hide certain widgets

        self.instructions_timer.timeout.connect(self.change_instructions)
        self.instructions_timer.timeout.connect(self.reset_input)  # resets user input of suspense

        self.my_widget = KeyboardWidget(self.window)  # will set focus to this after suspense is recorded

    def ask_suspense(self):
        self.window.lbl_suspense.setText("How much suspense do you feel now?")
        self.window.lbl_suspense_scale.setText("1 = no suspense\n3 = moderate suspense \n5 = extreme suspense")
        self.ui.unhide_suspense_widgets()
        self.verify_suspense_input()

    def verify_suspense_input(self):
        self.suspense = self.window.txt_suspense.text().strip()

        if self.suspense:  # if there is an input
            try:  # using a try except in case user enters a non-integer, which would break the next line
                suspense_int = int(self.suspense)
                if suspense_int not in range(self.min_suspense, self.max_suspense + 1):
                    self.window.lbl_suspense.setStyleSheet("color: red;")
                    self.window.lbl_suspense.setText("Please enter a number from 1 to 5")
                else:
                    self.window.lbl_suspense.setStyleSheet("color: green;")
                    self.window.lbl_suspense.setText("Thank you!")
                    self.start_timer()
                    self.suspense_inputs.append(self.suspense)  # if no errors, record the input to list of suspense
                    self.check_num_inputs()  # checks if max num of trials has been hit

            except ValueError:
                self.window.lbl_suspense.setStyleSheet("color: red;")
                self.window.lbl_suspense.setText("Please enter a valid number")

    def reset_input(self):
        self.window.txt_suspense.setReadOnly(True)  # stopping further input and resetting the text
        self.window.txt_suspense.setText("")
        self.my_widget.setFocus()  # changing the focus from the line edit to the window

    def start_timer(self):
        self.instructions_timer.start(self.instructions_delay)

    def change_instructions(self):
        self.ui.hide_suspense_widgets()
        self.window.lbl_spin_instructions.setText(
            "Press and hold 'c' to spin the spinner.\nPressing longer will make it spin faster.")
        self.window.lbl_spin_instructions.show()
        self.instructions_timer.stop()

    def check_num_inputs(self):  # emitted list of suspense will be used to record results to a results file
        if len(self.suspense_inputs) == self.max_trials:
            self.suspense_inputs_complete.emit(self.suspense_inputs)


