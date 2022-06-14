# traning the model FC-NN-NODE

import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import BatchNormalization, Dense, LeakyReLU
from tensorflow.keras.callbacks import ModelCheckpoint

# hidden dims for FC-NN-NODE is 672 (see supporting information of manuscript)
hidden_dims = 672
leaky_alpha = 0.3
batch_size = 512
epoch = 200

# you can change the number in model_full_path for different model
data_path = '/nn_data/original_data/'
model_full_path = '/nn_model/model_same_nodes_1.h5'

data_in = np.load(data_path+'data_in.npy')
data_out = np.load(data_path+'data_out.npy')

data_num = data_in.shape[0]

# split training, validation and test data
vali_start = int(data_num*7/9)
test_start = int(data_num*8/9)

data_in_train = data_in[:vali_start,:,:]
data_out_train = data_out[:vali_start,:,:]
data_in_vali = data_in[vali_start:test_start,:,:]
data_out_vali = data_out[vali_start:test_start,:,:]
data_in_test = data_in[test_start:,:,:]
data_out_test = data_out[test_start:,:,:]

train_num = data_in_train.shape[0]
vali_num = data_in_vali.shape[0]
test_num = data_in_test.shape[0]
height = data_in_train.shape[1]
input_dim = data_in_train.shape[2]
output_dim = data_out_train.shape[2]

# stack the input and output profiles into a single vector
train_in = np.zeros([train_num,input_dim*height])
train_out = np.zeros([train_num,output_dim*height])
vali_in = np.zeros([vali_num,input_dim*height])
vali_out = np.zeros([vali_num,output_dim*height])
test_in = np.zeros([test_num,input_dim*height])
test_out = np.zeros([test_num,output_dim*height])

for i in range(input_dim):
    train_in[:,i*height:(i+1)*height] = data_in_train[:,:,i]
    vali_in[:,i*height:(i+1)*height] = data_in_vali[:,:,i]
    test_in[:,i*height:(i+1)*height] = data_in_test[:,:,i]

for i in range(output_dim):
    train_out[:,i*height:(i+1)*height] = data_out_train[:,:,i]
    vali_out[:,i*height:(i+1)*height] = data_out_vali[:,:,i]
    test_out[:,i*height:(i+1)*height] = data_out_test[:,:,i]

# model structure for FC-NN-NODE, which has 10 layers
model = Sequential()

model.add(Dense(hidden_dims, input_shape = (input_dim*height,)))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(hidden_dims))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.add(Dense(output_dim*height))
model.add(BatchNormalization())
model.add(LeakyReLU(leaky_alpha))

model.compile(loss='mse', optimizer = 'rmsprop')

# only the best model on validation data is saved
save_best = ModelCheckpoint(model_full_path, verbose = 2, save_best_only = True)
model.fit(train_in,train_out,batch_size=batch_size,epochs=epoch,verbose=2,validation_data=(vali_in,vali_out),shuffle=True,callbacks = [save_best])

test_loss = model.test_on_batch(test_in,test_out)

print('same nodes complete model training!')
