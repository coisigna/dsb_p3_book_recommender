import pandas as pd
import numpy as np
import streamlit as st

def data_cleanse(csv):

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

    # Filter and sort analysis dataframe

    df_analysis = df_analysis[(df_analysis["numRatings"]> 100)&(df_analysis["rating"]>0)].sort_values("numRatings", ascending=False)
    
    df_analysis.reset_index(drop=True)

    df_analysis.rename(columns = {"index" : "book_index"})

    return df_analysis

def get_dict(row):
    try:
        l_cleaned = eval(row)
    except:
        l_cleaned = {}
    return l_cleaned

def genres_to_cols(df):

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

    return df_resulted 

def pages_to_cols(df, df_with_genres):

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

    df_resulted = pd.merge(left=df_with_genres, right=df_pages, how="inner", left_index=True, right_index=True)
    df_resulted = df_resulted.drop("title_y", axis = 1)
    df_resulted = df_resulted.rename(columns={"title_x":"title"})

    return df_resulted

def create_weighted_genre_matrix(df_ui, df_main):

    df_resulted = pd.merge(left = df_ui, right = df_main, how = "outer", on = "title")
        
    l_weighted_genre_matrix = list()

    for rating, genres in zip(df_resulted[df_resulted["rating"]>0]["rating"].values, df_resulted.iloc[:,2:].values):
        l_weighted_genre_matrix.append(rating*genres)

    df_weighted_genre_matrix = pd.DataFrame(l_weighted_genre_matrix, columns = df_resulted.iloc[:,2:].columns)

    return df_resulted, df_weighted_genre_matrix

def create_weighted_books_matrix(df):
    
    st.write(df.sum())
    
    s_user_weights = df.sum()

    s_user_weights = s_user_weights/s_user_weights.sum()

    df_recommendation = df[~(df["rating"] > 0)]

    weighted_books_matrix = list()

    for j in df_recommendation.iloc[:, 2:].values:
        weighted_books_matrix.append(s_user_weights.values*j)
        
    df_weighted_books_matrix = pd.DataFrame(data = weighted_books_matrix, columns = df.iloc[:,2:].columns)

    return df_weighted_books_matrix

def create_recommendation_dataframe(df_start,df_weighted_books_matrix):

    df_recommendation = pd.concat([df_start[["title","author", "description", "awards", "isbn", "coverImg"]], df_weighted_books_matrix.sum(axis = 1)], axis = 1).sort_values(0, ascending = False)
    df_recommendation.rename(columns={0:"coincidence_rating"}, inplace=True)

    return df_recommendation





    

