from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#* Read data
df = pd.read_csv("C:/Users/pauli/virtualenviroment/venvModule/Datasets/Spotify_Song_Attributes.csv")

#* Clean data
df = df.drop(['msPlayed', 'type', 'id', 'analysis_url', 'uri', 'track_href', 'duration_ms'], 
             axis='columns')
df = df.replace('NaN', pd.NA)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

#* No limits on columns display
pd.set_option('display.max_columns', None)

#* Data preparation
    #* Get rid of spaces in between artist and apply lower case
df["trackName"] = df["trackName"].str.lower()
# df["artistName"] = df["artistName"].str.replace(" ", "")
df["artistName"] = df["artistName"].str.lower()
df["genre"] = df["genre"].str.lower()

    #* Combine all columns and assgin as new column
df["data"] = df.apply(lambda value: " ".join(value.astype("str")), axis=1)

#* Models
vectorizer = CountVectorizer()
vectorized = vectorizer.fit_transform(df["data"])
similarities = cosine_similarity(vectorized)

#* Assgin new dataframe with 'similarities' values
df_tmp = pd.DataFrame(similarities, columns=df["trackName"], index=df["trackName"]).reset_index()
df_tmp = pd.merge(df_tmp, df[['trackName', 'artistName']], on='trackName', how='left')

true = True
while true:
    print("The Top 10 Song Recommendation System")
    print("-------------------------------------")
    print("This will generate the 10 songs from the database thoese are similar to the song you entered.")

    # Asking the user for a song, it will loop until the song name is in our database.
    while True:
        input_song = input("Please enter the name of song: ")

        if input_song in df_tmp.columns:
            recommendation = df_tmp.nlargest(11, input_song)[["trackName", "artistName"]]
            break
        
        else:
            print("Sorry, there is no song name in our database. Please try another one.")
    
    print("You should check out these songs: \n")
    for song in recommendation.values[1:]:
        print(song)

    print("\n")
    # Asking the user for the next command, it will loop until the right command.
    while True:
        next_command = input("Do you want to generate again for the next song? [yes, no] ")

        if next_command == "yes":
            break

        elif next_command == "no":
            # `true` will be false. It will stop the whole script
            true = False
            break

        else:
            print("Please type 'yes' or 'no'")
