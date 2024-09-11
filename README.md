**Prerequisites**

•	pip install pyqt6  <br>
• To install the PyQT Designer:  <br>
Download the appropriate version from https://build-system.fman.io/qt-designer-download



**Experiment overview**

The code provided can be used to investigate the affective state of suspense.  The experiment created is a replication of experiment one in Zhi-Wei and colleagues’ 2019 study, with a few minor modifications made. In this experiment, the researchers took games that the theoretical model of suspense predicted to be extremely high/low in suspense. They then asked participants to play these games and self-report their levels of suspense throughout the game. The model also predicts step by step fluctuations in suspense, which can also be compared to the participants’ reports of suspense.

**Experimenter’s manual**

•Open the main file of the program and navigate to the experiment setup section (lines 20-40). <br>
•	Here you can change the name of the results file that is output by the program. It is set to ExperimentResults.csv by default.  You do not need to create this file, the program will automatically create the file with the name you have given on the first run.<br>
•	Set max_trials to be the number of card draws you would like the participants to complete. This is set to 5 by default. <br>
•	You may change the cards in the deck by changing card_deck. Note that you should not add more than 9 values as this would require changes in the UI file to display more cards. Feel free to change the card values.<br>
•	Please input the cards that you would like to be selected per trial for each condition (i.e., in cards_drawn_high_suspense and cards_drawn_low_suspense). Do not set max_trials to be greater than 5 if you have not added the cards to be drawn on rounds after 5. The card selection is predefined and not randomly generated since we are experimentally controlling the cards participants draw.<br>
•	Input the conditions you would like to run this experiment for, default is set to high suspense and low suspense, but conditions can be easily added with the following three changes.<br>
•	If you would like to add another condition, please add the new conditions to the conditions list. <br>
•	Then create a new set of card selections per trial for this condition in the same format as the high and low conditions given.<br>
•	Lastly, you will need to add the new condition and corresponding card selection you have created to card_draws_per_condition. If adding a new condition, please ensure the name in card_draws_per_condition matches the name you have given the condition. You do not need to change any other part of the program to cater for a new condition.<br>
•	Once you have made any required changes, you are ready to start the experiment. 
•	Once each participant is ready, all you need to do is hit play and a user interface will pop up.
•	The following results will be stored in a file in wide format, i.e., a single row per participants: condition, demographic information, self-reported measures of suspense on each trial.


