import pandas as pd
import numpy as np
import streamlit as st

def data_cleanse(csv):

    '''
    It transforms csv file to a dataframe and cleans it filtering what it s not needed and preparing what it is.

    ## Parameters

    csv : CSV File with goodreads information

    '''

    # Dataframes creation

    df, df_analysis, df_discarded = pd.read_csv(csv), pd.read_csv(csv), pd.read_csv(csv)

    # Creating a dataframe with all the discarded columns

    df_discarded = df[["bookId","series","characters","bookFormat","edition","publisher","publishDate","firstPublishDate","setting","price"]]

    # Dropping discarded columns from the analysis dataframe

    df_analysis = df.drop(df_discarded.columns, axis = 1)

    # likedPercent has Nan's and we can use rating instead
    # bbeScore isn't scaled and we can use rating instead
    # bbeVotes values are much lower than numRatings ones
    # ratingsByStars could be useful in df_user but not in df_analysis

    df_analysis.drop(["likedPercent","bbeScore","bbeVotes","ratingsByStars"], axis = 1, inplace= True)

    # Deleting those without specified language

    df_analysis = df_analysis[df_analysis["language"].isnull() == False].reset_index(drop=True)

    # Deleting those without specified pages

    df_analysis = df_analysis[df_analysis["pages"].isnull() == False].reset_index(drop=True)

    # Deleting those without specified genres

    df_analysis = df_analysis[df_analysis["genres"] != "[]"].reset_index(drop = True)

    # Join title and author in the same column

    l_new_title = []

    for title, author in zip(df_analysis["title"],df_analysis["author"]):
        
        l_new_title.append(' - '.join((title,author)))
        
    df_analysis["title"] = l_new_title

    df_analysis.drop("author", axis = 1, inplace=True)

    df_analysis.drop_duplicates(keep = False, inplace=True)

    df_analysis.reset_index(drop = True, inplace = True)

    # Filter and sort analysis dataframe

    df_analysis = df_analysis[(df_analysis["numRatings"]> 100)&(df_analysis["rating"]>0)].sort_values("numRatings", ascending=False)
    
    df_analysis.reset_index(drop = False, inplace = True)

    df_analysis.rename(columns = {"index" : "book_index"}, inplace = True)

    return df_analysis

def get_dict(row):

    '''
    It evaluates the object that is inside of a str and returns it.

    ## Parameters

    row : Row of a column that needs to be evaluated
    '''

    try:
        l_cleaned = eval(row)
    except:
        l_cleaned = {}
    return l_cleaned

def genres_to_cols(df):

    '''
    It transforms the column genres into 50 different columns for the 50 most popular genres of the data. Every row of every column will be filled either with a 1 or 0 as the book contains than genre or not.

    ## Parameters

    df : dataframe with the column genres
    '''

    l_cleaned_categories = list()
    for i in df["genres"]:
        l_cleaned_categories.append(get_dict(i))

    l_unique_categories = list()
    for i in l_cleaned_categories:
        
        for j in i:
            l_unique_categories.append(j)

    s_unique_categories = set(l_unique_categories)

    # Counting most common genres

    d_cont = {i:0 for i in s_unique_categories}
    for i in l_cleaned_categories:
        for j in i:
            d_cont[j] = d_cont[j] + 1

    l_sorted_categories = list(sorted(d_cont.items(), key=lambda item: item[1]))
    l_sorted_categories = l_sorted_categories[::-1]

    l_sorted_categories = [j[0] for j in l_sorted_categories[:50]]

    l_datos = list()


    for row in l_cleaned_categories:

        
        l_categorias_peliculas = list()
        
        for cat in l_sorted_categories:
        
            if cat in row:
                l_categorias_peliculas.append(1)

            else:

                l_categorias_peliculas.append(0)

        l_datos.append(l_categorias_peliculas)

    df_resulted = pd.DataFrame(data = l_datos, columns = l_sorted_categories)

    df_resulted.insert(0, 'title', df["title"])  
    df_resulted.insert(0, 'book_index', df["book_index"])  

    return df_resulted 

def pages_to_cols(df, df_with_genres):

    '''
    It transforms the column pages into 3 different columns for the 3 categories it has been decided to divide it (short for pages < 200, medium for 200 <= pages < 50 and large for pages >500).
    Every row will be filled either with a 1 or 0 as the book fits in one of the 3 categories.
    Once it is done, the function merges it with the dataframe of the genres in order to create the matrix for the recomendation.

    ## Parameters

    df : dataframe with the column pages
    df_with_genres : genres dataframe previously treated

    '''

    df["pages"]=df["pages"].apply(lambda x: x.split()[0] if pd.notnull(x) else x)
    df["pages"]=df["pages"].apply(lambda x: int(x) if pd.notnull(x) else x)

    l_pages = list()

    for i in df["pages"]:
        
        if i < 200:

            l_pages.append("short")

        elif 200 <= i < 500:

            l_pages.append("medium")

        elif i >= 500:

            l_pages.append("large")

        else:

            l_pages.append(np.nan)

    df_pages = pd.DataFrame()

    df_pages["title"] = df["title"]
    df_pages["short"] = [1 if i == "short" else 0 for i in l_pages]
    df_pages["medium"] = [1 if i == "medium" else 0 for i in l_pages]
    df_pages["large"] = [1 if i == "large" else 0 for i in l_pages]

    df_pages.insert(0, 'book_index', df["book_index"])  

    df_resulted = pd.merge(left=df_with_genres, right=df_pages, how="inner", on="book_index")

    df_resulted.drop(["book_index","title_y"],axis=1, inplace=True)

    df_resulted.rename(columns={"title_x":"title"}, inplace=True)

    return df_resulted

def create_weighted_genre_matrix(df_ui, df_main):

    '''
    It creates a weighted genre matrix from two input dataframes, the one created from the input of the user and the one returned from pages_to_cols(df, df_with_genres).
    It merges the two dataframes and stores the result in df_resulted
    Then it multiplies the "rating" by the corresponding genre values and stores the result in a list l_weighted_genre_matrix.
    Finally, it converts l_weighted_genre_matrix into a dataframe df_weighted_genre_matrix and returns both df_resulted and df_weighted_genre_matrix.

    ## Parameters

    df_ui : dataframe created from the inputs of the user
    df_main : dataframe returned from pages_to_cols(df, df_with_genres)
    '''

    df_resulted = pd.merge(left = df_ui, right = df_main, how = "outer", on = "title")
        
    l_weighted_genre_matrix = list()

    for rating, genres in zip(df_resulted[df_resulted["rating"]>0]["rating"].values, df_resulted.iloc[:,2:].values):
        l_weighted_genre_matrix.append(rating*genres)

    df_weighted_genre_matrix = pd.DataFrame(l_weighted_genre_matrix, columns = df_resulted.iloc[:,2:].columns)

    return df_resulted, df_weighted_genre_matrix

def create_weighted_books_matrix(df_weighted_genre_matrix, df_ui):

    '''
    It calculates the sum of the values in df_weighted_genre_matrix along axis 0 (rows) and normalizes the sum by dividing it by its sum. This gives the user weights.
    Then it multiplies the user weights  by the corresponding genre values and returns the result transformed into a dataframe.

    ## Parameters

    df_weighted_genre_matrix : dataframe returned from create_weighted_genre_matrix(df_ui, df_main)
    df_ui : dataframe created from the inputs of the user
    '''
        
    s_user_weights = df_weighted_genre_matrix.sum()

    s_user_weights = s_user_weights/s_user_weights.sum()

    df_recommendation = df_ui[~(df_ui["rating"] > 0)]

    weighted_books_matrix = list()

    for j in df_recommendation.iloc[:, 2:].values:
        weighted_books_matrix.append(s_user_weights.values*j)
        
    df_weighted_books_matrix = pd.DataFrame(data = weighted_books_matrix, columns = df_ui.iloc[:,2:].columns)

    return df_weighted_books_matrix

def create_recommendation_dataframe(df_start,df_weighted_books_matrix):

    '''
    It creates the dataframe with recomendation.

    ## Parameters

    df_start : dataframe returned from data_cleanse(csv)

    df_weighted_books_matrix : dataframe returned from create_weighted_books_matrix(df_weighted_genre_matrix, df_ui)

    '''

    df_recommendation = pd.concat([df_weighted_books_matrix.sum(axis = 1), df_start[["title", "description", "awards", "isbn", "coverImg", "numRatings", "rating"]]], axis = 1)
    df_recommendation.rename(columns={0:"coincidence_rating"}, inplace=True)

    df_recommendation = df_recommendation.sort_values(["coincidence_rating", "numRatings"], ascending = False)

    return df_recommendation.head(5)





    

