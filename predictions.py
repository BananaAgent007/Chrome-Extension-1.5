import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
def predictTimes(training, sample):
  data = np.array(training)
  X = data[:, 1:]  # Features: average word length, total word count, readability score
  y = data[:, 0]   # Target variable: read time
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)
  # Create an SVR model and train it using original dataset
  svr = SVR(kernel='rbf') 
  svr.fit(X_scaled, y)
  # Make predictions for new data points
  new_data_point = np.array(sample)
  scaled_new_data_point = scaler.transform(new_data_point.reshape(1, -1))
  predicted_read_time = svr.predict(scaled_new_data_point)
  print("prediction: ", predicted_read_time[0])
  return np.int32(predicted_read_time[0])