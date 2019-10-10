#Importing data
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('rating.csv')
movies_df.head()

movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)
#Removing the parentheses
movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)
#Removing the years from the 'title' column
movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')
movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())
movies_df.head()

#Every genre is separated by a |
movies_df['genres'] = movies_df.genres.str.split('|')
movies_df.head()

#Copying the movie dataframe into a new one
moviesWithGenres_df = movies_df.copy()

for index, row in movies_df.iterrows():
    for genre in row['genres']:
        moviesWithGenres_df.at[index, genre] = 1
#Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
moviesWithGenres_df = moviesWithGenres_df.fillna(0)
moviesWithGenres_df.head()

ratings_df.head()

ratings_df = ratings_df.drop('timestamp', 1)
ratings_df.head()

userInput = [
            {'title':'Breakfast Club, The', 'rating':5},
            {'title':'Toy Story', 'rating':3.5},
            {'title':'Jumanji', 'rating':2},
            {'title':"Pulp Fiction", 'rating':5},
            {'title':'Akira', 'rating':4.5}
         ] 
inputMovies = pd.DataFrame(userInput)
inputMovies

#Filtering out the movies by title
inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
inputMovies = pd.merge(inputId, inputMovies)

inputMovies = inputMovies.drop('genres', 1).drop('year', 1)

#Final input dataframe
inputMovies

userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
userMovies

#Resetting the index to avoid future issues
userMovies = userMovies.reset_index(drop=True)

userGenreTable = userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
userGenreTable

inputMovies['rating']

userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
#The user profile
userProfile

genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
genreTable = genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
genreTable.head()

genreTable.shape


recommendationTable_df = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommendationTable_df.head()
#Sorting recommendations in descending order
recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
recommendationTable_df.head()

#The final recommendation table
r = movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(20).keys())]
print(r)
