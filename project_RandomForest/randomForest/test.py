import pandas

games = pandas.read_csv("board_games.csv")
print(games.columns)
print(games.shape)


# import matplotlib.pyplot as plt
# # Plot a histogram of all the ratings in the average_rating column.
# plt.hist(games["average_rating"])

#plt.show()
# Print the first row of all the games with zero scores.
# Dataframes.iloc: Purely integer-location based indexing for selection by position.

#print(games[games["average_rating"] == 0].iloc[-1])
# Print the first row of all the games with scores greater than 0.
#print(games[games["average_rating"] > 0].iloc[-1])



#Remove any rows with "average_rating"] == 0
games = games[games["users_rated"] > 0]
# Remove any rows with missing values.
#print (games.shape)
games = games.dropna(axis=0)
#print (games.shape)

# from sklearn.cluster import KMeans
#
# kmeans_model = KMeans(n_clusters=5, random_state=1)
# #Get only the numeric columns from games.
# good_columns = games._get_numeric_data()
# # Fit the model using the good columns.
# kmeans_model.fit(good_columns)
# # Get the cluster assignments.
# labels = kmeans_model.labels_
# print labels



from sklearn.cross_validation import train_test_split
games = games.sample(frac=0.1,random_state=1)
# Set random_state to be able to replicate results.
train = games.sample(frac=0.8, random_state=1)
# Select anything not in the training set and put it in the testing set.
test = games.loc[~games.index.isin(train.index)]
print(train.shape)
print(test.shape)




# Get all the columns from the dataframe.
columns = games.columns.tolist()
# Filter the columns to remove ones we don't want.
columns = [c for c in columns if c not in ["bayes_average_rating", "average_rating", "type", "name"]]
# Store the variable we'll be predicting on.
target = "average_rating"

train_X = train[columns].as_matrix()
train_y = train[target].as_matrix()
test_X = test[columns].as_matrix()
test_y = test[target].as_matrix()


#random forest classifier

# from forest import RandomForestClassifier
# rfc_model = RandomForestClassifier()
# rfc_model.fit(train_X,train_y)
# accuracy = rfc_model.score(test_X,test_y)
# print 'The accuracy was', accuracy, ' on the test data.'
# forest = RandomForestClassifier(n_estimators=10)
# forest.fit(train[columns],train[target])
# rfc_prediction = forest.predict_proba(test[columns])


from sklearn.ensemble import RandomForestClassifier
rfr_model = RandomForestClassifier(n_estimators=30, min_samples_leaf=10, random_state=1)
rfr_model.fit(train_X,train_y)
accuracy =  rfr_model.score(test_X,test_y)
print accuracy

# rfr_model.fit(train[columns], train[target])
# rfr_predictions = rfr_model.predict(test[columns])
# accuracy =  rfr_model.score(test[columns],test[target])
# Import the random forest model.
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# rfr_model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
# rfr_model.fit(train[columns], train[target])
# rfr_predictions = rfr_model.predict(test[columns])
# accuracy =  rfr_model.score(test[columns],test[target])
# print accuracy
# # Compute the error.
# re = mean_squared_error(rfr_predictions, test[target])
# print re
# print rfr_predictions
