import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import flask as fl

# Create Dataframe
df = pd.read_csv('C:/Users/Keegan/OneDrive/Desktop/sample_data_sets/books.csv')

# Remove Columns
to_drop = [ 
    'language_code',
    'isbn13',
    'isbn',
    'authors',
    'bookID',
    'average_rating',
    'Unnamed: 12',
    'Unnamed: 13',
    'Unnamed: 14'
]
df.drop( to_drop, inplace=True, axis=1)


# extract date and year from columns for merge
df['Dates_v1'] = pd.to_datetime( df['publisher'], errors='coerce' ).dt.date 
df['Dates_v1'] = np.where( df['Dates_v1'].isna(), np.nan, df['Dates_v1'] )
df['Dates_v1'] = pd.to_datetime( df['Dates_v1'], errors='coerce' ).dt.year
df['publication_year'] = df['publication_date'].str[-4:].astype(int)
df['year'] = df['Dates_v1'].combine_first( df['publication_year'] ).astype(int)

# drop unneeded columns related to date
to_drop = [
    'publication_date',
    'publication_year',
    'Dates_v1'
]
df.drop( to_drop, inplace=True, axis=1)

# Change date values in publisher column to null
df['publisher'] = np.where( df['publisher'].str.match( '\d{2}/\d{2}/\d{4}'), np.nan, df['publisher'] )

# remove leading or trailing spaces from headers
df.columns = df.columns.str.strip()

# adjust column data types for calc later
def to_int(x):
    try:
        return int(x)
    except( ValueError, TypeError):
        return None  
df['num_pages'] = df['num_pages'].fillna(0)  
df['num_pages'] = df['num_pages'].apply(to_int) 

df['average_rating'] = df['num_pages'].fillna(0)
df['average_rating'] = df['num_pages'].apply(to_int)

df['ratings_count'] = df['ratings_count'].fillna(0)
df['ratings_count'] = df['ratings_count'].apply(to_int)

df['text_reviews_count'] = df['text_reviews_count'].fillna(0)
df['text_reviews_count'] = df['text_reviews_count'].apply(to_int)

# drop all na values 
df.dropna()

# define quantiles and IQR for page_num
Q1 = df['num_pages'].quantile(0.25)
Q2 = df['num_pages'].quantile(0.50)
Q3 = df['num_pages'].quantile(0.75)
IQR = Q3 - Q1

# define quartiles and IQR for year
yr_Q1 = df['year'].quantile(0.25)
yr_Q2 = df['year'].quantile(0.50)
yr_Q3 = df['year'].quantile(0.75)
yr_IQR = yr_Q3 - yr_Q1

# define quartiles and IQR for ratings_count
rc_Q1 = df['ratings_count'].quantile(0.25)
rc_Q2 = df['ratings_count'].quantile(0.50)
rc_Q3 = df['ratings_count'].quantile(0.75)
rc_IQR = rc_Q3 - rc_Q1

# define quartiles and IQR for text_reviews
tr_Q1 = df['text_reviews_count'].quantile(0.25)
tr_Q2 = df['text_reviews_count'].quantile(0.50)
tr_Q3 = df['text_reviews_count'].quantile(0.75)
tr_IQR = tr_Q3 - tr_Q1
 
# num_page limit based on IQR 
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR
outliers_low = ( df['num_pages'] < lower_limit )
outliers_high = ( df['num_pages'] > upper_limit )

# year limit based on IQR
yr_lower_limit = yr_Q1 - 1.5 * yr_IQR
yr_upper_limit = yr_Q3 + 1.5 * yr_IQR
yr_outliers_low = ( df['year'] < yr_lower_limit )
yr_outliers_high = ( df['year'] > yr_upper_limit )

# rating_count limit based on IQR
rc_lower_limit = rc_Q1 - 1.5 * rc_IQR
rc_upper_limit = rc_Q3 + 1.5 * rc_IQR
rc_outliers_low = ( df['ratings_count'] < rc_lower_limit )
rc_outliers_high = ( df['ratings_count'] > rc_upper_limit )

# text_review limit based on IQR
tr_lower_limit = tr_Q1 - 1.5 * tr_IQR
tr_upper_limit = tr_Q3 + 1.5 * tr_IQR
tr_outliers_low = ( df['text_reviews_count'] < rc_lower_limit )
tr_outliers_high = ( df['text_reviews_count'] > rc_upper_limit )

# adjust the dataframe to exclude records with outlier values
df = df[~( outliers_low )]
df = df[~( outliers_high )]
df = df[~( yr_outliers_low )]
df = df[~( yr_outliers_high )]
df = df[~( rc_outliers_low )]
df = df[~( rc_outliers_high )]
df = df[~( tr_outliers_low )]
df = df[~( tr_outliers_high )]

#print( df['num_pages'] )

# // Helper stuff // #
# How to Find rows where values are not numeric (or a specific datatype)
# non_numeric_rows = df[~df['num_pages'].str.isnumeric()]
df.to_csv('C:/Users/Keegan/OneDrive/Desktop/sample_data_sets/books_adj.csv', index=False)


