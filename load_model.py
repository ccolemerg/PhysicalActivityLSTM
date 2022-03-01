import numpy as np
from tensorflow import keras
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import math


def two_digit_converter(self):
    return "%0.1f" % self


input_x = np.asarray(test_walking).astype(np.float32)
input_x = input_x.reshape((1, 24, 1))

reconstructed_model_walking = keras.models.load_model("models/model-11-03-2021-03-36-50.h5")


predictions = reconstructed_model_walking.predict(input_x)

print('prediction')
print(predictions)
predictions = predictions[:, :, 0]
predictions = predictions.reshape(24, 1)


print(predictions)

for i in range(len(predictions)):
    #predictions[i] = round(predictions[i])
    predictions[i] = two_digit_converter(predictions[i])


print(predictions)


print('tilting root mean squared error')
print(math.sqrt(mean_squared_error(predictions_tilting, real_data_tilting)))
print('tilting mean absolute error')
print(mean_absolute_error(predictions_tilting,real_data_tilting))



days = np.arange(0, 24, 1).tolist()

plt.clf()


plt.plot(days, predictions_vehicle,  color='#33cc00', label='Forecasted',marker='^', linewidth=1.8)
plt.plot(days, real_data_vehicle, color='#ff4dff', label='Actual',marker='*', linewidth=1.8)


plt.xlabel('Hours',  fontsize=13, color='#000066', weight='bold')
plt.ylabel('Physical Activity Duration(Minutes)', fontsize=13, color='#000066', weight='bold')

plt.yticks(weight='bold')
plt.xticks(weight='bold')


plt.rcParams["font.size"] = "11.0"
plt.rcParams["font.weight"] = "bold"

plt.legend()


plt.savefig('tilting_24hours.png', dpi=400)


plt.show()




