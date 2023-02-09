# Introduction

In this Readme we're about to explain all the technical information related with the project development. If you're looking for the fundamentals, motivation or management, [this](https://github.com/coisigna/dsb_p3_book_recommender/wiki) is your site!

- Colab and try yourself the code used for analyzing, plotting or doing your own recommender.

The dataset used for this project has been dwonloaded from [Kaggle](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b), well-known wed in the data science world where you can find a huge variety of datasets.

# Usage

### At first, you have to look for a book you like, and select it in the select box. 

<br>

![alt image](/resources/select_book.gif)

### After selecting the book, you have to give it a rating. The more books you vote, the better the recommendation will be.

<br>

![alt image](/resources/vote_book.gif)

<br>



### When you have voted all your books, just click recommendation and enjoy the results!

<br>

![alt image](/resources/gen_recommendation.gif)

<br>


# EDA and first developement (Book recomender.ipynb)

The development of the entire project, depended on the results obtained in the EDA (Exploratory Data Analysis) stage. 

[Here](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/ipynbs/Book%20recomender.ipynb) it can be found the reasons of choosing some features and discarding others and the ways that problems have been solved during the proces, check the full study if you are interested.


# Main ([main.py](https://github.com/coisigna/dsb_p3_book_recommender/blob/main/pys/main.py))

### st.session_state

This feature has been used to store the main variables in order to avoid rerunning them everytime the streamlit page refreshes.

```python
st.session_state['df_cleansed'] = data_cleanse(csv) 
```

### st.tabs

It is used to divide the interfaz in different tabs, two in this project.

```python
tab_vote, tab_recommendation = st.tabs(["Vote books","recommendation"])
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

It creates a button widget that the user can click to perform a specific action. In this case to vote and to generate the recommendation.

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
st.success("Success!! Your recomendatión is ready, go to the next tab to check it!")
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
