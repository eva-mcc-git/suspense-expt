
class Results:
    def __init__(self, filename, condition):
        self.filename = filename
        self.condition = condition
        self.suspense = None
        self.demog_info = None

    def update_suspense(self, suspense_values):  # connected in the main file to a signal output by suspense class
        self.suspense = suspense_values

    def update_demog_info(self, inputs):  # also connected in main file to signal output by user inputs
        self.demog_info = inputs

    def record_results(self):  # writes to our file
        file_handle = open(self.filename, 'a')
        all_info = []  # will add all demographic info and suspense responses to a list

        for value in self.demog_info.values():
            all_info.append(str(value))
        for suspense_responses in self.suspense:
            all_info.append(str(suspense_responses))

        all_info.insert(0, self.condition)  # adding condition to the list
        file_handle.write(",".join(all_info) + "\n")  # converting to a string to write to the file
        file_handle.close()

