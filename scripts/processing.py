import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn import metrics


def train_model(inputs, targets):
    model = LogisticRegression()
    model.fit(inputs, targets)
    return model

def transform_data() :
    pre_processed_df = pd.read_csv('preprocessed_data.csv')

    """We will use logistic regression to classify people of the data into classes"""

    # creating the target for logistic regression
    # We define an Abstenteeism of more than 3 hours like Excessive

    median = pre_processed_df['Absenteeism Time in Hours'].median()
    targets = np.where(pre_processed_df['Absenteeism Time in Hours']>3, 1, 0) # if time of absenteeism  3 hours transform into 1 else transform into 0
    pre_processed_df['Excessives absenteeism'] = targets

    # Removed 'Absenteeism Time in Hours' column

    data_with_targets = pre_processed_df.drop(columns='Absenteeism Time in Hours')



    unseperated_inputs = data_with_targets.iloc[:,:-1]

    # Standardization of non-separated inputs
    absenteeism_scaler = StandardScaler()

    absenteeism_scaler.fit(unseperated_inputs) #Calculate the mean and the std for  next standardizations

    scaled_inputs = absenteeism_scaler.transform(unseperated_inputs) 


    # Splitting data into training and testing sets : 80 % of the data for trainning and 20% for testing

    train_inputs, test_inputs, train_targets, test_targets = train_test_split(scaled_inputs, targets, train_size=0.8, random_state = 20 )

    return train_inputs, test_inputs, train_targets, test_targets







if __name__ == "__main__":
    # Training the model on the training data
    train_inputs, test_inputs, train_targets, test_targets = transform_data()
    reg_model = train_model( train_inputs, train_targets )


    accuracy = reg_model.score(train_inputs, train_targets)














