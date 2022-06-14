# for 1D-CNN training
# one-dimensional convolutional neural network (1D-CNN)
# this is also the DeepBL in the manustript

import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, ZeroPadding1D, BatchNormalization, LeakyReLU
from tensorflow.keras.callbacks import ModelCheckpoint

# model parameters of channel size, kernel size, etc
filter_num = 56
kernel_size = 3

padding_val = 2
strides_num = 1

kernel_ini_style = 'glorot_uniform'
bias_ini_style = 'zeros'
leaky_alpha = 0.3

batch_size = 512
epoch = 200

# you can change the number in model_full_path to get different NN
data_path = '/nn_data/original_data/'
model_full_path = '/nn_model/model_original_1.h5'

data_in = np.load(data_path+'data_in.npy')
data_out = np.load(data_path+'data_out.npy')

data_num = data_in.shape[0]

# 7/9 of data for training, 1/9 for validation, last 1/9 for testing
# but only training and validation data are used for 1D-CNN training
vali_start = int(data_num*7/9)
test_start = int(data_num*8/9)

# read in data and split it into training, validation and test data
data_in_train = data_in[:vali_start,:,:]
data_out_train = data_out[:vali_start,:,:]
data_in_vali = data_in[vali_start:test_start,:,:]
data_out_vali = data_out[vali_start:test_start,:,:]
data_in_test = data_in[test_start:,:,:]
data_out_test = data_out[test_start:,:,:]

height = data_in_train.shape[1]
channel_in = data_in_train.shape[2]
channel_out = data_out_train.shape[2]

# 1D-CNN structure, which has 10 layer.
# schematic diagram is shown in the manuscript
model = Sequential()

model.add(Conv1D(filter_num, kernel_size, \
          input_shape = (height, channel_in), strides = strides_num, padding = 'valid', \
		  use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Conv1D(filter_num, kernel_size, strides = strides_num, padding = 'same', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(ZeroPadding1D(padding_val))
model.add(Conv1D(channel_out, kernel_size, strides = strides_num, padding = 'valid', \
          use_bias = True, kernel_initializer=kernel_ini_style, bias_initializer=bias_ini_style))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

# loss: mse; optimization scheme: rmsprop
model.compile(loss='mse', optimizer = 'rmsprop')

# only the best model on validation set is saved
save_best = ModelCheckpoint(model_full_path, verbose = 2, save_best_only = True)

model.fit(data_in_train,data_out_train,batch_size=batch_size,epochs=epoch,verbose=2,\
validation_data=(data_in_vali,data_out_vali),shuffle=True,callbacks=[save_best])

print('10l56c-complete model training!')
