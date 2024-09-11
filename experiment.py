class Experiment:
    def __init__(self, filename, conditions):
        self.filename = filename
        self.conditions = conditions
        self.condition_count = dict()

    def create_file(self, data): # consider separating from this class
        if len(data) == 0:
            headers = ['Condition',
                       'Name',
                       'Age',
                       'Gender',
                       'Education Level',
                       'Suspense 1',
                       'Suspense 2',
                       'Suspense 3',
                       'Suspense 4',
                       'Suspense 5']
            file_handle = open(self.filename, 'a')
            file_handle.write(",".join(headers) + "\n")
            file_handle.close()

    def read_file(self):
        try:  # using a try except here because if the file does not exist it cannot read it and will cause a break
            file_handle = open(self.filename, 'r')
            self.data = file_handle.readlines()
            file_handle.close()

        except FileNotFoundError:
            self.data = []
            self.create_file(self.data)  # only gets called if there is no file
        return self

    def initialise_condition_count(self):  # set count to 0 for all conditions
        for condition in self.conditions:
            self.condition_count[condition] = 0

    def get_condition_count(self):
        all_data = []

        for row in self.data: # converting string of data into a list of lists. Wide format: each list represents one participant
            if '\n' in row:
                new_row = row.strip('\n')
            participant_data = new_row.split(',')
            all_data.append(participant_data)

        # the following condition counter is written to dynamically accept more conditions
        for i in range(1, len(all_data)):  # looping through rows of participant data
            condition = all_data[i][0]  # first item on the list is condition
            self.condition_count[condition] += 1  # find the key for that condition and add 1 to the value
        return self

    def assign_condition(self):
        # using get to find values associated with each key and iterating through them to find the min
        # and then returning the associated key. Doing it this way to make it dynamic, so all you have to
        # do when adding a new condition is change init
        self.assigned_condition = min(self.condition_count, key=self.condition_count.get)
        return self

    def run_experiment_setup(self):
        self.read_file()
        self.initialise_condition_count()
        self.get_condition_count()
        self.assign_condition()

