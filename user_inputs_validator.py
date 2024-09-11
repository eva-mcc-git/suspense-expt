from ui import *
from PyQt5.QtCore import *


class UserInputsValidator(QObject):
    valid_user_inputs = pyqtSignal(dict)
    consent_given = pyqtSignal()

    def __init__(self, window):
        super(UserInputsValidator, self).__init__()
        self.window = window
        self.trial_num = 1  # initialising at 1, but will update as we go

        self.ui = Ui(self.window)  # creating an instance to highlight fields missing user inputs
        self.demog_info = dict()

        self.window.btn_next.clicked.connect(self.check_inputs)
        self.window.rdb_consent.stateChanged.connect(self.check_consent_errors)  # used to remove error msgs after button is ticked

    def check_consent_errors(self):
        error_msg = "Please consent to the terms to continue."
        if not self.window.rdb_consent.isChecked():
            error = True
            self.ui.highlight_border(self.window.rdb_consent, error)  # highlights the consent box in red
            self.window.lbl_consent_error.setText(error_msg)
        else:
            error = False
            self.consent_given.emit()
            self.ui.highlight_border(self.window.rdb_consent, error)  # undoes the red highlight
            self.window.lbl_consent_error.setText("")
        return error

    def get_demog_inputs(self):
        name = self.window.txt_name.text().strip()
        age = self.window.spn_age.value()
        education = self.window.cmb_education.currentText()
        gender = self.window.cmb_sex.currentText()
        return {"name": name, "age": age, "gender": gender, "education": education}

    def check_demog_errors(self):  # checks the participant has given the demographic info
        inputs = self.get_demog_inputs()
        missing_fields = []
        under_16 = False  # specifying that the participant must be over 16 to partake

        if not inputs["name"]:  # checks for any name input
            missing_fields.append("name")  # creating a list of missing fields to notify the user of which to fill in
            self.ui.highlight_border(self.window.txt_name, True)  # there is an error -> highlight
        else:
            self.ui.highlight_border(self.window.txt_name, False)  # no error, un-highlight

        if inputs["age"] == 0:
            missing_fields.append("age")
            self.ui.highlight_border(self.window.spn_age, True)
        elif inputs["age"] < 16:
            self.window.lbl_error.hide()
            self.window.lbl_age_error.setText("You must be over 16 to take part. Please close the experiment window.")
            under_16 = True
        else:
            self.ui.highlight_border(self.window.spn_age, False)
            self.window.lbl_error.show()
            self.window.lbl_age_error.hide()
            under_16 = False

        if not inputs["gender"]:
            missing_fields.append("sex")
            self.ui.highlight_border(self.window.cmb_sex, True)
        else:
            self.ui.highlight_border(self.window.cmb_sex, False)

        if not inputs["education"]:
            missing_fields.append("education")
            self.ui.highlight_border(self.window.cmb_education, True)
        else:
            self.ui.highlight_border(self.window.cmb_education, False)

        if missing_fields or under_16:
            missing_fields_str = " and ".join(missing_fields)
            error_msg = f"Please enter {missing_fields_str} to continue."  # tell participant which fields are missing info
            self.window.lbl_error.setText(error_msg)
            errors = True
        else:
            errors = False
            self.valid_user_inputs.emit(inputs)

        return errors

    def check_inputs(self):  # connected to the next button, so if the user tries to continue, we check their inputs
        current_page = self.window.stacked_widget.currentIndex()
        if current_page == 0:
            self.check_consent_errors()
        elif current_page == 1:
            self.check_demog_errors()







