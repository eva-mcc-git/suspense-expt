from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Ui:
    def __init__(self, window):
        self.window = window

        self.arrow_timer = QTimer()
        self.pulse_speed = 300  # the speed of the flashing red arrow
        self.pulse_count = 0  # keeps track of number of pulses
        self.arrow_timer.timeout.connect(self.flashing_arrow)
        self.window.btn_start.clicked.connect(self.stop_timer)

        # the following attributes are used to control when the user can change page
        self.consent_given = False
        self.valid_inputs = False
        self.experiment_ended = False

# ------------ Everything in this section relates to setup/reset for next card draw ------------
    def run_ui_setup(self):
        self.set_pixmaps()
        self.trial_reset()

    def set_pixmaps(self):
        # creating parallel lists
        image_labels = [self.window.lbl_red_arrow,
                        self.window.lbl_ucl_logo,
                        self.window.lbl_wheel,
                        self.window.lbl_wheel_arrow,
                        self.window.lbl_arrow1,
                        self.window.lbl_arrow2]
        image_pixmaps = ["red-arrow.png",
                         "UCL.png",
                         "wheel.png",
                         "wheel_arrow.png",
                         "arrow.png",
                         "arrow.png"]
        for i in range(len(image_labels)):
            image_labels[i].setPixmap(QPixmap(image_pixmaps[i]))

    def trial_reset(self):
        self.hide_suspense_widgets()
        self.hide_widgets()
        self.display_instructions()
        self.reset_inputs()
        self.reset_txt_colours()
        self.start_timer()  # triggers flashing arrow

    def hide_suspense_widgets(self):  # hides the widgets related to the self-report of suspense, these will be shown later
        self.window.txt_suspense.hide()
        self.window.lbl_suspense.hide()
        self.window.lbl_suspense_scale.hide()

    def hide_widgets(self):  # hides other instruction widgets
        self.window.lbl_spin_instructions.hide()  # instructs user to press c to spin the wheel
        self.window.lbl_next_round.hide()  # instructions after a card draw round has complete

    def display_instructions(self):  # very first instruction given
        self.window.lbl_next_round.setText("Press shuffle to draw two cards.")
        self.window.lbl_next_round.show()

    def reset_inputs(self):  # reset user input for suspense
        self.window.txt_suspense.setText("")

    def reset_txt_colours(self):  # reset fields that were highlighted red due to errors
        black = "color: black;"
        self.window.lbl_sum.setStyleSheet(black)
        self.window.txt_suspense.setStyleSheet(black)
        self.window.lbl_suspense.setStyleSheet(black)

# ---------------------- Other Ui related methods ---------------------------------
    def unhide_suspense_widgets(self):  # widgets related to pop up for self-reported suspense survey
        self.window.txt_suspense.show()
        self.window.lbl_suspense.show()
        self.window.lbl_suspense_scale.show()
        self.window.txt_suspense.setReadOnly(False)  # unlocks so user can input a suspense value

    def highlight_border(self, widget, condition):  # used to highlight fields the participant has not filled in (Demographic info) & unhighlight when they are filled
        border_color = 'red' if condition else ''
        border_style = f"border: 1px solid {border_color};" if condition else ''
        widget.setStyleSheet(border_style)

    def update_consent(self):  # used in page_change_checks, connected to a signal emitted by consent being given
        self.consent_given = True

    def update_valid_inputs(self):  # used in page_change_checks, connected to a signal emitted by valid demog inputs being given
        self.valid_inputs = True

    def end_game(self, total):
        self.window.btn_start.hide()
        self.experiment_ended = True

        if total >= 21:  # if participant loses
            self.window.lbl_next_round.setText(f"Your final score is {total}, resulting in a bust.\n Please click next to continue to experiment debrief.")
        else:  # win
            self.window.lbl_next_round.setText(
                f"Your final score is {total}, congratulations on your win!\n Please click next to continue to experiment debrief.")
        self.window.lbl_next_round.show()

    def page_change_checks(self):
        page_index = self.window.stacked_widget.currentIndex()

        if page_index == 0 and self.consent_given:
            self.change_page(page_index)
        elif page_index == 1 and self.valid_inputs:
            self.change_page(page_index)
        elif page_index == 2:  # expt description page, no checks
            self.change_page(page_index)
        elif page_index == 3 and self.experiment_ended:
            self.change_page(page_index)
            self.window.btn_next.setText("Finish")
        elif page_index == 4:
            self.window.close()

    def change_page(self, page_index):
        self.window.stacked_widget.setCurrentIndex(page_index + 1)

# ----------- This remaining methods all relates to the flashing red arrow -------------
    def start_timer(self):
        self.arrow_timer.start(self.pulse_speed)

    def stop_timer(self):
        self.arrow_timer.stop()
        self.window.lbl_red_arrow.hide()

    def flashing_arrow(self):
        self.pulse_count += 1

        if self.pulse_count % 2 == 0:
            self.window.lbl_red_arrow.show()
        else:
            self.window.lbl_red_arrow.hide()



