## Building a Regression Model in Keras

# Project Description
In this project, I built a regression model using the Keras library to predict the strength of concrete. The project includes data analysis, building models with different architectures, and evaluating their performance.

# Project Structure
The project consists of four tasks, each completed in a separate Jupyter Notebook:

- Building a Basic Model
A base model with one hidden layer (10 nodes, ReLU activation) was built.
The data was split into training and testing sets, and the mean square error (MSE) was estimated.

- Using the normalized version of the data
The data was normalized (subtracting the mean and dividing by the standard deviation).
The model was trained on normalized data with 50 epochs.

- Using 100 epochs for training
The model was trained on normalized data, but the number of epochs was increased to 100.
The results were compared with the previous task.

- Increasing the number of hidden layers
A model with three hidden layers (10 nodes each, ReLU activation) was built.
The impact of the larger architecture on the mean square error was evaluated.

# Tools and Technologies
Python
Pandas
NumPy
TensorFlow / Keras
Scikit-learn
