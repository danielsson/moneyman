moneyman
========

moneyman automatically categorizes and graphs your bank account transaction history, giving you a quick and cool
overview of your spending habits. How much did you spend on coffee last month? Was it more than the month before?

Quick setup guide
------------------
0. Clone this project to a destination of your choosing
1. Install dependencies:(Sklearn wouldn't install to my virtualenv)

        pip install flask flask-login sklearn

2. Take a look at transactionTypes in ```moneyman/predictor/classifier_utils.py``` You may customize the
    dict if you like. You'll use these values in the next step.
3. Next we must create a training set for the predictor. This is done by exporting ~100 account transactions to
a .csv file. The rows must look like the following example:

        2013-01-30, some transaction message, 2785.75, 6
Where the 6 at the end is the category you want the row to be filed in. The numbers are those found int the file in step 2.
4. The easiest way to train the predictor is to rename and move the csv-file you've just created to ```moneyman/predictor/export.csv```. Then, from the same directory, run the command
        
        cd moneyman/predictor/
        python classifier_utils.py
If you dont want to move the file, you can manually train the classifier using the function train_classifier_with_csv found in classifier_utils.py using the python shell.

5. Now its time to create the database and start the app! Do so by running:

        cd ../
        sqlite3 moneyman.db < transactions.sql
        python app.py
        
6. Go to the url displayed after running the previous command, and press Transactions in the main menu.
7. Upload your account transactions using the button Upload CSV.

Done!
