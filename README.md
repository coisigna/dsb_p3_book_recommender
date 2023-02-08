# Introduction

In this Readme we're about to explain all the technical information related with the project development. If you're looking for the fundamentals, motivation or management, [this](https://github.com/coisigna/dsb_p3_book_recommender/wiki) is your site!

- Colab and try yourself the code used for analyzing, plotting or doing your own recommender.

The dataset used for this project has been dwonloaded from [Kaggle](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b), well-known wed in the data science world where you can find a huge variety of datasets.

# EDA and firs developement

The development of the entire project, depended on the results obtained in the EDA (Exploratory Data Analysis) stage. [Here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/ipynbs/Book%20recomender.ipynb) it can be found the reasons of choosing some features and discarding others and the ways that problems have been solved during the proces, check the full study if you are interested.

# my_funcs.py

Check it [here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/pys/my_funcs.py)

### data_cleanse(csv)
```python
It transforms csv file to a dataframe and cleans it filttering what it s not needed and preparing what it is.

Requirements:
csv =
```
### get_dict(row)

It evaluates the object that is inside of a str and returns it.

Requirements:

row = (row of a column that needs to be evaluated)

### genres_to_cols(df)

It transforms the column genres into 50 different columns for the 50 most popular genres of the data. Every row of every column will be filled either with a 1 or 0 as the films contains than genre or not.

Requirements:

df = (dataframe with the column genres)

### pages_to_cols(df, df_with_genres)

It transforms the column pages into 3 different columns for the 3 categories it has been decided to divide it (short for pages < 200, medium for 200 <= pages < 50 and large for pages >500).
Every row will be filled either with a 1 or 0 as the book fits in one of the 3 categories.
Once it is done, the function merges it with the dataframe of the genres in order to create the matrix for the recomendation.

Requirements:

df = (dataframe with the column pages)
df_with_genres = (genres dataframe previously treated)

### create_weighted_genre_matrix(df_ui, df_main)

It creates a weighted genre matrix from two input dataframes, the one created from the input of the user and the one returned from pages_to_cols(df, df_with_genres).
It merges the two dataframes and stores the result in df_resulted
Then it multiplies the "rating" by the corresponding genre values and stores the result in a list l_weighted_genre_matrix.
Finally, it converts l_weighted_genre_matrix into a dataframe df_weighted_genre_matrix and returns both df_resulted and df_weighted_genre_matrix.

Requirements:

df_ui = (dataframe created from the inputs of the user)
df_main = (dataframe returned from pages_to_cols(df, df_with_genres))

### create_weighted_books_matrix(df_weighted_genre_matrix, df_ui)

It calculates the sum of the values in df_weighted_genre_matrix along axis 0 (rows) and normalizes the sum by dividing it by its sum. This gives the user weights.
Then it multiplies the user weights  by the corresponding genre values and returns the result transformed into a dataframe.

Requirements:

df_weighted_genre_matrix = (dataframe returned from create_weighted_genre_matrix(df_ui, df_main))
df_ui = (dataframe created from the inputs of the user)

### create_recommendation_dataframe(df_start,df_weighted_books_matrix)

It creates the dataframe with recomendation.

Requirements:

df_start = (dataframe returned from data_cleanse(csv))

df_weighted_books_matrix = (dataframe returned from create_weighted_books_matrix(df_weighted_genre_matrix, df_ui))

