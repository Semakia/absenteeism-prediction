
import pandas as pd

# Importing data
absenteeism_df = pd.read_csv('Absenteeism-data.csv') 

# Preprocessing the data
def prepare_data(df) :
    
    #dropping ID column

    df.drop(columns='ID', inplace=True)

    #transform column reason for absences into dummies values
    reason_columns = pd.get_dummies(df['Reason for Absence'])

    #Group the values ​​into 4 groups
    Reason_1 = reason_columns.iloc[:, 1:14].max(axis=1)
    Reason_2 = reason_columns.iloc[:, 15:17].max(axis=1)
    Reason_3 = reason_columns.iloc[:, 18:21].max(axis=1)
    Reason_4 = reason_columns.iloc[:, 22:29].max(axis=1)

    




    df.drop(columns='Reason for Absence', inplace=True ) 

    preprocessing_df = pd.concat([Reason_1, Reason_2, Reason_3, Reason_4, df], axis=1)


    preprocessing_df.columns = ['Reason 1', 'Reason 2', 'Reason 3', 'Reason 4' ,'Date' ,'Transportation Expense', 'Distance to Work', 'Age',
    'Daily Work Load Average', 'Body Mass Index' ,'Education' ,'Children' , 'Pets','Absenteeism Time in Hours']

    print(preprocessing_df.columns.values)

    preprocessing_df['Date'] = pd.to_datetime(preprocessing_df['Date'], format="%d/%m/%Y")


    # Extracting month value and day value from date column 

    list_of_months , list_of_days = [] , []
    for index  in range(700):
        list_of_months.append(preprocessing_df['Date'][index].month)

    
    for index  in range(700):
        list_of_days.append(preprocessing_df['Date'][index].day)

    preprocessing_df.drop(columns="Date", inplace=True)


    df = pd.DataFrame({'month value': list_of_months, 'day of week': list_of_days})
    preprocessing_df = pd.concat([df, preprocessing_df], axis=1)


    # Turn education into binary data 
    for index in range(700):
        if preprocessing_df['Education'][index] == 1 :
            preprocessing_df['Education'][index] =0
        else :
            preprocessing_df['Education'][index] = 1
    
    # Reordering columns of the dataset
            
    columns_ordered = ['Reason 1', 'Reason 2', 'Reason 3', 'Reason 4' ,'month value', 'day of week' ,'Transportation Expense', 'Distance to Work', 'Age',
    'Daily Work Load Average', 'Body Mass Index' ,'Education' ,'Children' , 'Pets','Absenteeism Time in Hours']
    preprocessing_df = preprocessing_df[columns_ordered]


    return preprocessing_df



final_data = prepare_data(absenteeism_df)
final_data.to_csv('E:/Projets Data/absenteism-pre-procesing/preprocessing_data.csv', index=False)