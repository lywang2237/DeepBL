# generate nonlinearly transformed data
# calculate the changed stds and avgs and save
# here take n=0.6, which is the optimal value in the manuscript
# you can also change the n for different data

import numpy as np

input_path = '/nn_data/raw_data/'
data_in_path = '/nn_data/original_data/'
output_path = '/nn_data/nonli_trans/0.6/'

# input data is not transformed, just copy from original data (simple normalization)
# output data is transformed, read in raw data of output for further processing
data_in = np.load(data_in_path+'data_in.npy')
data_out = np.load(input_path+'data_out.npy')

output_dim = data_out.shape[2]

# nonlinear transformation
# power function of the original value and maintain the signs
# nonlinear transformation happens before normalization and will
# change the stds and avgs of the output
data_out = np.multiply(np.sign(data_out),np.power(np.abs(data_out),0.6))

# for saving of changed stds and avgs
turflux_avg_all = np.zeros([output_dim,])
turflux_std_all = np.zeros([output_dim,])

# stds and avgs are calculated on training and validation data only
train_vali_start = int((data_in.shape[0])*8/9)

# calculate stds and avgs
for h in range(output_dim):
    turflux_avg_all[h] = np.mean(data_out[:train_vali_start,:,h])
    turflux_std_all[h] = np.sqrt(np.mean(np.square(data_out[:train_vali_start,:,h] - turflux_avg_all[h])))
    data_out[:,:,h] = (data_out[:,:,h]-turflux_avg_all[h])/turflux_std_all[h]

# save
np.save(output_path+'data_in',data_in)
np.save(output_path+'data_out',data_out)
np.save(output_path+'turflux_avg',turflux_avg_all)
np.save(output_path+'turflux_std',turflux_std_all)
