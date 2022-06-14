# processing for training validation and test data

import numpy as np
from netCDF4 import Dataset

# average scale (number of grid point) and the radius (km) of the circular region for data acquisition
avg_scale = 20
radius_real = 80

input_path = '/avg_data/'
output_path = '/nn_data/raw_data/'

# get domain size
input_ins = Dataset(input_path+'avg_large_14:00:00.nc').variables['u']
nz = 14
ny = input_ins.shape[1]
nx = input_ins.shape[2]

# calculate the number of grid point of the real radius length
# get the coordinate of the center of the circle region
radius = np.floor(radius_real/(avg_scale*0.1))
rx = np.floor(nx/2)
ry = np.floor(ny/2)

# get all the valid coordinates that are in the circular region
valid_list = []
for i in range(nx):
    for j in range(ny):
        if (rx-i)**2+(ry-j)**2 <= radius**2:
            valid_list.append([i,j])

# length of this list is the data number of a single time output
num_per_frame = len(valid_list)

# 9 hours in total, 6 outputs per hour, so in total num_per_frame*9*6
# 6 inputs, U,V,W,TH,Q,Qc
# 4 outputs, uw, vw, thw, qvw
data_in = np.zeros((num_per_frame*9*6,nz,6))
data_out = np.zeros((num_per_frame*9*6,nz,4))

# transform the original data into training/validation/test data
frame_count = 0
for hid in range(14,24):
    for mid in range(0,6):

        if hid == 19 and mid == 3:
            continue

        frame_count += 1
        TURFLUX = Dataset(input_path+'avg_flux_all_'+str(hid)+':'+str(mid)+'0:00.nc')
        LARGE = Dataset(input_path+'avg_large_'+str(hid)+':'+str(mid)+'0:00.nc')
        uw = TURFLUX.variables['uw'][:]
        vw = TURFLUX.variables['vw'][:]
        thw = TURFLUX.variables['thw'][:]
        qvw = TURFLUX.variables['qvw'][:]
        u = LARGE.variables['u'][:]
        v = LARGE.variables['v'][:]
        w = LARGE.variables['w'][:]
        th = LARGE.variables['th'][:]
        qv = LARGE.variables['qv'][:]
        qc = LARGE.variables['qc'][:]
        
        # get all the data points in the circular region into the data_in and data_out
        for i in range(num_per_frame):
            data_in[num_per_frame*(frame_count-1)+i,:,0] = u[:,valid_list[i][1],valid_list[i][0]]
            data_in[num_per_frame*(frame_count-1)+i,:,1] = v[:,valid_list[i][1],valid_list[i][0]]
            data_in[num_per_frame*(frame_count-1)+i,:,2] = w[:,valid_list[i][1],valid_list[i][0]]
            data_in[num_per_frame*(frame_count-1)+i,:,3] = th[:,valid_list[i][1],valid_list[i][0]]
            data_in[num_per_frame*(frame_count-1)+i,:,4] = qv[:,valid_list[i][1],valid_list[i][0]]
            data_out[num_per_frame*(frame_count-1)+i,:,0] = uw[:,valid_list[i][1],valid_list[i][0]]
            data_out[num_per_frame*(frame_count-1)+i,:,1] = vw[:,valid_list[i][1],valid_list[i][0]]
            data_out[num_per_frame*(frame_count-1)+i,:,2] = thw[:,valid_list[i][1],valid_list[i][0]]
            data_out[num_per_frame*(frame_count-1)+i,:,3] = qvw[:,valid_list[i][1],valid_list[i][0]]

        print('Task '+str(hid)+':'+str(mid)+'0:00 is finished')
		
        if hid == 23:
            break
	
	if hid == 23:
            break

# save data_in as raw input and output (not normalized)
# we can choose to normalize directly to get simple normalized data
# we can also choose to first nonlinearly transforme it and then normalize it to get nonlinearly transformed data
np.save(output_path+'data_in',data_in)
np.save(output_path+'data_out',data_out)

# training and validation data number
# standard deviations and averages are calculated only on the training and validation data
train_vali_num = num_per_frame*8*6

# calculation of global std and avgs, and calculation of per-level std and avgs
large_avg = np.zeros([nz,5])
turflux_avg = np.zeros([nz,4])
large_std = np.zeros([nz,5])
turflux_std = np.zeros([nz,4])
large_avg_all = np.zeros([5,])
large_std_all = np.zeros([5,])
turflux_avg_all = np.zeros([4,])
turflux_std_all = np.zeros([4,])
for n in range(5):
    for h in range(nz):
        large_avg[h,n]=np.sum(data_in[:train_vali_num,h,n],axis=None)/train_vali_num
for n in range(4):
    for h in range(nz):
        turflux_avg[h,n]=np.sum(data_out[:train_vali_num,h,n],axis=None)/train_vali_num

for n in range(5):
    for h in range(nz):
        large_std[h,n]=np.sqrt(np.sum(np.square(data_in[:train_vali_num,h,n]-large_avg[h,n]))/train_vali_num)
for n in range(4):
    for h in range(nz):
        turflux_std[h,n]=np.sqrt(np.sum(np.square(data_out[:train_vali_num,h,n]-turflux_avg[h,n]))/train_vali_num)

for n in range(5):
    large_avg_all[n] = np.sum(data_in[:train_vali_num,:,n],axis=None)/(train_vali_num*nz)
for n in range(4):
    turflux_avg_all[n] = np.sum(data_out[:train_vali_num,:,n],axis=None)/(train_vali_num*nz)

for n in range(5):
    large_std_all[n] = np.sqrt(np.sum(np.square(data_in[:train_vali_num,:,n]-large_avg_all[n]),axis=None)/(train_vali_num*nz))
for n in range(4):
    turflux_std_all[n] = np.sqrt(np.sum(np.square(data_out[:train_vali_num,:,n]-turflux_avg_all[n]),axis=None)/(train_vali_num*nz))

# save the stds and avgs
np.save(output_path+'large_avg',large_avg)
np.save(output_path+'turflux_avg',turflux_avg)
np.save(output_path+'large_std',large_std)
np.save(output_path+'turflux_std',turflux_std)
np.save(output_path+'large_avg_all',large_avg_all)
np.save(output_path+'turflux_avg_all',turflux_avg_all)
np.save(output_path+'large_std_all',large_std_all)
np.save(output_path+'turflux_std_all',turflux_std_all)
