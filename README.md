# Introduction

In this Readme we're about to explain all the technical information related with the project development. If you're looking for the fundamentals, motivation or management, [this](https://github.com/coisigna/dsb_p3_book_recommender/wiki) is your site!

- Colab and try yourself the code used for analyzing, plotting or doing your own recommender.

The dataset used for this project has been dwonloaded from [Kaggle](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b), well-known wed in the data science world where you can find a huge variety of datasets.

# EDA and firs developement (Book recomender.ipynb)

The development of the entire project, depended on the results obtained in the EDA (Exploratory Data Analysis) stage. [Here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/ipynbs/Book%20recomender.ipynb) it can be found the reasons of choosing some features and discarding others and the ways that problems have been solved during the proces, check the full study if you are interested.

# Functions (my_funcs.py)

Check it [here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/pys/my_funcs.py)

### data_cleanse(csv)
```
It transforms csv file to a dataframe and cleans it filttering what it s not needed and preparing what it is.

Requirements:
csv =
```
### get_dict(row)
```
It evaluates the object that is inside of a str and returns it.

Requirements:

row = (row of a column that needs to be evaluated)
```
### genres_to_cols(df)
```
It transforms the column genres into 50 different columns for the 50 most popular genres of the data. Every row of every column will be filled either with a 1 or 0 as the films contains than genre or not.

Requirements:

df = (dataframe with the column genres)
```
### pages_to_cols(df, df_with_genres)
```
It transforms the column pages into 3 different columns for the 3 categories it has been decided to divide it (short for pages < 200, medium for 200 <= pages < 50 and large for pages >500).
Every row will be filled either with a 1 or 0 as the book fits in one of the 3 categories.
Once it is done, the function merges it with the dataframe of the genres in order to create the matrix for the recomendation.

Requirements:

df = (dataframe with the column pages)
df_with_genres = (genres dataframe previously treated)
```
### create_weighted_genre_matrix(df_ui, df_main)
```
It creates a weighted genre matrix from two input dataframes, the one created from the input of the user and the one returned from pages_to_cols(df, df_with_genres).
It merges the two dataframes and stores the result in df_resulted
Then it multiplies the "rating" by the corresponding genre values and stores the result in a list l_weighted_genre_matrix.
Finally, it converts l_weighted_genre_matrix into a dataframe df_weighted_genre_matrix and returns both df_resulted and df_weighted_genre_matrix.

Requirements:

df_ui = (dataframe created from the inputs of the user)
df_main = (dataframe returned from pages_to_cols(df, df_with_genres))
```
### create_weighted_books_matrix(df_weighted_genre_matrix, df_ui)
```
It calculates the sum of the values in df_weighted_genre_matrix along axis 0 (rows) and normalizes the sum by dividing it by its sum. This gives the user weights.
Then it multiplies the user weights  by the corresponding genre values and returns the result transformed into a dataframe.

Requirements:

df_weighted_genre_matrix = (dataframe returned from create_weighted_genre_matrix(df_ui, df_main))
df_ui = (dataframe created from the inputs of the user)
```
### create_recommendation_dataframe(df_start,df_weighted_books_matrix)
```
It creates the dataframe with recomendation.

Requirements:

df_start = (dataframe returned from data_cleanse(csv))

df_weighted_books_matrix = (dataframe returned from create_weighted_books_matrix(df_weighted_genre_matrix, df_ui))
```


# Main (main.py)

Check it [here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/pys/main.py)

### st.session_state

This feature has been used to store the main variables in order to avoid rerunning them everytime the streamlit page refreshes.

```python
st.session_state['df_cleansed'] = data_cleanse(csv) 
```

### st.tabs

It is used to divide the interfaz in different tabs, two in this project.

```python
tab_vote, tab_recomendation = st.tabs(["Vote books","Recomendation"])
```

### st.selectbox

It creates a dropdown selection widget that allows the user to select one item from a list of options. In this case, books.

```python
sb_book = st.selectbox('Select the book', options = st.session_state['df_main']["title"].values)
```

### st.slider

It creates a slider widget that allows the user to select a value from a range by sliding a handle along a track.In this case, punctuation of the book.

```python
sl_punctuation = st.slider("Select punctuation", 0, 10)
```

### st.button

It creates a button widget that the user can click to perform a specific action. In this case to vote and to generate the recomendation.

```python
bu_vote = st.button("Vote",help="")
```

### st.table

It creates a table from a pandas dataframe or a list of lists, which can be used to display tabular data in a readable and organized format. In this case, books and punctuation voted by the user

```python
st.table(data=st.session_state['df_user_input'])
```

### st.success

It creates a success message, which is used to provide feedback to the user that an action was successful. Success messages are typically displayed in green.

```python
st.success("Succes!! Your recomendatión is ready, go to the next tab to check it!")
```

### st.markdown

It creates a markdown element, which allows you to format text, create headings, and add links, images, and other elements to your Streamlit app. In this project, it has been used for displaying images.

```python
st.markdown(f"![Alt text]({df_recommendation['coverImg'].iat[1]})") 
```

### st.write

It writes any type of object to the app, including text, dataframes, plots, and more. It's a versatile function that's useful for a variety of tasks.In this project it has only been used for displaying text.

```python
st.write(df_recommendation["description"].iat[1])
```