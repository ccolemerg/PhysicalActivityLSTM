from math import sqrt
from numpy import split
from numpy import array
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.layers import ConvLSTM2D, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers import Activation, Masking, Dense, SimpleRNN
from keras.layers import Bidirectional
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from datetime import datetime
import math
from sklearn.metrics import mean_absolute_error


timesteps_count = 24

train_b_index = 0
train_e_index = 0 + (timesteps_count * half_days)
test_b_index = train_e_index + 0
test_e_index = test_b_index + timesteps_count

real_b_index = test_e_index + 0
real_e_index = real_b_index + timesteps_count


def performance_forecasts(actual, predicted):
    scores = list()

    for i in range(actual.shape[1]):
        mse = mean_squared_error(actual[:, i], predicted[:, i])
        rmse = sqrt(mse)
        scores.append(rmse)

    s = 0
    for row in range(actual.shape[0]):
        for col in range(actual.shape[1]):
            s += (actual[row, col] - predicted[row, col]) ** 2
    score = sqrt(s / (actual.shape[0] * actual.shape[1]))
    return score, scores

def supervised_data(train, n_input, n_out=timesteps_count):
    data = train.reshape((train.shape[0] * train.shape[1], train.shape[2]))
    X, y = list(), list()
    in_start = 0
    for _ in range(len(data)):
        in_end = in_start + n_input
        out_end = in_end + n_out
        if out_end <= len(data):
            x_input = data[in_start:in_end, current_column]
            x_input = x_input.reshape((len(x_input), 1))
            X.append(x_input)
            y.append(data[in_end:out_end, current_column])


        in_start += 1

    return array(X), array(y)


def supervised_data_test(test, n_input, n_out=timesteps_count):
    data = train.reshape((train.shape[0] * train.shape[1], train.shape[2]))
    print(len(data))
    X, y = list(), list()
    in_start = 0

    for _ in range(len(data) - n_out - 1):
        in_end = in_start + n_input
        out_end = in_end + n_out

        x_input = data[in_start:in_end, current_column]
        x_input = x_input.reshape((len(x_input), 1))
        X.append(x_input)
        y.append(data[in_end:out_end, 1])

        in_start += 1

    print('-----------Train x -------------')
    print(X)
    print('-----------Train y -------------')
    print(y)
    return array(X), array(y)


def plot_validation(history):
    plt.clf()
    loss = history.history['loss']
    history_dict = history.history
    print(history_dict.keys())
    print(loss)
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, 'g', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()


# train the model
def get_model(train, n_steps, n_length, n_input, test):

    train_x, train_y = supervised_data(train, n_input)
    train_x = np.asarray(train_x).astype(np.float32)
    train_y = np.asarray(train_y).astype(np.float32)
  
    test_x, test_y = supervised_data_test(test, n_input)

    n_timesteps, n_features, n_outputs = test_x.shape[1], test_x.shape[2], test_y.shape[0]

    test_x = test_x.reshape((test_x.shape[0], n_steps, 1, n_length, n_features))

    # define parameters
    verbose, epochs, batch_size = 2, 100, 24
    n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]
    x0 = train_x.shape[0]
    x1 = train_x.shape[1]
    print(len(train_x[0]))
    print(x0)
    print(x1)
    train_x = train_x.reshape(train_x.shape[0], train_x.shape[1], n_features)

    print(train_x)

    train_y = train_y.reshape((train_y.shape[0], train_y.shape[1], n_features))



    model = Sequential()
    model.add(LSTM(256, input_shape=(n_timesteps, n_features), return_sequences=True))
    model.add(LSTM(128, return_sequences=True))
    model.add(LSTM(64, return_sequences=True))
    model.add(TimeDistributed(Dense(32, activation='relu')))
    model.add(TimeDistributed(Dense(n_features)))
    model.compile(loss='mse', optimizer='adam',  metrics=['accuracy'])
    model.summary()

    history = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    model_path_str = "models/model-" + dt_string + ".h5"
    model.save(model_path_str)


    return model



def forecast_lstm(model, history, n_steps, n_length, n_input):

    data = array(history)
    data = data.reshape((data.shape[0] * data.shape[1], data.shape[2]))
    input_x = test[:, :, current_column]
    input_x = np.asarray(input_x).astype(np.float32)
    input_x = input_x.reshape((1, n_length, 1))
    print(input_x)
    yhat = model.predict(input_x, verbose=0)
    yhat = yhat[0]

    return yhat


def evaluate_model(train, test, n_steps, n_length, n_input):
    model = build_model(train, n_steps, n_length, n_input, test)
    history = [x for x in train]
    predictions = list()
    for i in range(len(test)):
        yhat_sequence = forecast(model, history, n_steps, n_length, n_input)
        predictions.append(yhat_sequence)
        history.append(test[i, :])

    predictions = array(predictions)


    score, scores = evaluate_forecasts(test[:, :, 1], predictions)
    return score, scores, predictions



def predictions_with_dataset():
    dataset = read_csv('hourly_activity_minutes.txt', sep=';', header=0, low_memory=False, infer_datetime_format=True,
                   parse_dates={'datetime': [0, 1]}, index_col=['datetime'])

    print(dataset)

    train, test, real_data = split_dataset(dataset.values)
    n_steps, n_length = 1, timesteps_count
    n_input = n_length * n_steps
    score, scores, predictions = evaluate_model(train, test, n_steps, n_length, n_input)

    print(test[:, :, 1].shape)
    predictions = predictions.reshape(timesteps_count, 1)
    print('predictions')
    print(predictions)

    print('real data')
    real_data = real_data[:, :, current_column]
    print(real_data)
    real_data = real_data.reshape(timesteps_count, 1)

    days = np.arange(0, 24, 1).tolist()


    test = test[:, :, 0]
    test = test.reshape(timesteps_count, 1)

    hours_count = 24
    hours = []

    for i in range(hours_count):
        if i < 10:
        each_hours = "0" + str(i) + ":00"
        else:
        each_hours = str(i) + ":00"
        hours.append(each_hours)

    print('---mse---')
    print(mean_squared_error(real_data, predictions))
    print(sqrt(mean_squared_error(real_data, predictions)))
    print(mean_squared_error(test, predictions))
    print('---------')

    test_color = (0.2, 0.1, 0.6, 0.9)
    test_color_1 = (0.8, 0.1, 0.8, 0.6)


    # print(hours)
    plt.clf()
    plt.plot(days, predictions , color = test_color, label='Predicted')
    plt.plot(days, real_data, color=test_color_1, label='Actual')
    # plt.title('Prediction vs Real Values')
    plt.xlabel('Hours', fontweight='bold')
    plt.ylabel('Physical Activity Duration (Minutes)',fontweight='bold')
    plt.legend()
    plt.savefig('Walking.png')
    plt.show()

    print('walking root mean squared error')
    print(math.sqrt(mean_squared_error(real_data, predictions)))
    print('walking mean absolute error')
    print(mean_absolute_error(real_data,predictions))


if __name__ == "__main__":
   predictions_with_dataset()
 


