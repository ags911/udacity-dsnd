"""
Process Data
Project: Disaster Response Pipeline (Udacity - Data Science Nanodegree)
Sample Script Syntax:
> python train_classifier.py <path to messages csv> <path to categories csv> <path to sqllite destination db>
Sample Script Execution:
> python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
Arguments:
    1) Path to messages csv file
    2) Path to categories csv file
    3) Path to SQLite destination database (e.g. DisasterResponse.db)
"""

# import libraries
import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Load Data from csv Function
    
    Arguments:
        messages_filepath, categories_filepath
    Output:
        return df
    """
    
    # 1. load datasets
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    
    # 2. merge datasets
    df = pd.merge(messages, categories, how='left', on='id')
    
    return df
    

def clean_data(df):
    """
    Clean Data from csv Function
    
    Arguments:
        df -> dataframe containing disaster messages and categories
    Output:
        return df
    """
    
    # 3. split categories into separate category columns.
    categories = df['categories'].str.split(';', expand=True)
    row = categories.iloc[:1]
    category_colnames = row.values.tolist()[0] 
    category_colnames = [s.replace('-2', '').replace('-1', '').replace('-0', '') for s in category_colnames]
    categories.columns = category_colnames
    
    # 4. convert category values to just numbers 0 or 1
    for column in categories:
        categories[column] = categories[column].str.strip().str[-1]
        categories[column] = categories[column].astype(int)
        
    # 4.1 values other than 0 or 1 need to be corrected such as 2 to 1    
    categories = categories.replace(to_replace=2, value=1)

    # 5. replace categories column in df with new category columns
    df = df.drop(columns='categories')
    df1 = pd.concat([df, categories], axis=1, join='inner')
    df = df1

    # 5. remove duplicates
    df = df.drop_duplicates()
    
    # 6. remove child_alone since it has only zeros
    df = df.drop(['child_alone'], axis=1)
    
    return df

def save_data(df, database_filename):
    """
    Clean Data from csv Function
    
    Arguments:
        df -> dataframe containing disaster messages and categories
        database_filename -> filename of SQLLite database
    """
    
    engine = create_engine('sqlite:///'+ database_filename)
    table_name = database_filename.replace('.db','') + '_table'
    df.to_sql('DisasterResponse_table', engine, index=False, if_exists='replace')

def main():
    """
    Process Data Main Function
    
    This function applies the ETL process to the data:
        1) Load data from csv files
        2) Clean data from csv files
        3) Save data to SQLite database
    
    """
        
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
