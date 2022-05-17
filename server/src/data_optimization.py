from sklearn import preprocessing

# Standardization
preprocessing.scale(df)

# Normalization
preprocessing.normalize(df)

# Min-Max Scale
scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
scaler.fit_transform(df)