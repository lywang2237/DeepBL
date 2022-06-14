# simply normalize the data using stds and avgs

import numpy as np

input_path = '/nn_data/raw_data/'
output_path = '/nn_data/original_data/'

data_in = np.load(input_path+'data_in.npy')
data_out = np.load(input_path+'data_out.npy')

input_dim = data_in.shape[2]
output_dim = data_out.shape[2]

large_avg_all = np.load(input_path + 'large_avg_all.npy')
large_std_all = np.load(input_path + 'large_std_all.npy')
turflux_avg_all = np.load(input_path + 'turflux_avg_all.npy')
turflux_std_all = np.load(input_path + 'turflux_std_all.npy')

# normalization
for n in range(input_dim):
    data_in[:,:,n] = (data_in[:,:,n]-large_avg_all[n])/large_std_all[n]

for n in range(output_dim):
    data_out[:,:,n] = (data_out[:,:,n]-turflux_avg_all[n])/turflux_std_all[n]

# save
np.save(output_path+'data_in',data_in)
np.save(output_path+'data_out',data_out)
