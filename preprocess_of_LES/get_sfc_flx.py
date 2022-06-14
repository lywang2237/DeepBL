# get surface fluxes, uw vw thw qvw, from WRF LES output

import numpy as np
from netCDF4 import Dataset

data_path = '/tc_les/'
output_path = '/intrp/'

# Rd and Cp for calculation of surface fluxes
r_d = 287.04
cp = 1004.6

# cycling through 14:00:00 to 23:00:00
# 19:30:00 is skipped
for hid in range(14:24):
    for mid in range(6):
        
        # read in file and variables
        NC_FILE = Dataset(data_path+'wrfout_d04_2007-09-05_'+str(hid)+':'+str(mid)+'0:00')
        
        # only the variables in the first layer are requested
        # WRF output has data format (time, levels, south-north grid, west-east grid); 1 time per output so len(time) = 1
        ust = NC_FILE.variables['UST'][0,:,:]
        hfx = NC_FILE.variables['HFX'][0,:,:]
        qfx = NC_FILE.variables['QFX'][0,:,:]
        psfc = NC_FILE.variables['PSFC'][0,:,:]
        theta = NC_FILE.variables['T'][0,0,:,:] + 300.   # recover real potential temperature
        q = NC_FILE.variables['QVAPOR'][0,0,:,:]
        u = (NC_FILE.variables['U'][0,0,:,1:] + NC_FILE.variables['U'][0,0,:,:-1])/2.  # convert Aarakawa-C grid to Aarakawa-A grid
        v = (NC_FILE.variables['V'][0,0,1:,:] + NC_FILE.variables['V'][0,0,:-1,:])/2.

        ny = ust.shape[1]
        nx = ust.shape[0]
        
        # air density rho and Cpm
        rho = psfc/(r_d*theta)
        cpm = cp*(1+0.8*q)
        
        # calculation of uw vw thw and qvw
        uw_sf = -ust**2*u/np.sqrt(u**2+v**2)
        vw_sf = -ust**2*v/np.sqrt(u**2+v**2)
        thw_sf = hfx/cpm/rho
        qvw_sf = qfx/rho
        
        # write the surface fluxes to hard disk
        NC_OUTPUT = Dataset(output_path+'sfc_flx_'+str(hid)+':'+str(mid)+'0:00.nc','w',format = 'NETCDF4')

        NC_OUTPUT.createDimension('west_east',nx)
        NC_OUTPUT.createDimension('south_north',ny)

        NC_OUTPUT.createVariable('uw_sf',np.float32,('south_north','west_east'))
        NC_OUTPUT.createVariable('vw_sf',np.float32,('south_north','west_east'))
        NC_OUTPUT.createVariable('thw_sf',np.float32,('south_north','west_east'))
        NC_OUTPUT.createVariable('qvw_sf',np.float32,('south_north','west_east'))

        NC_OUTPUT.variables['uw_sf'][:] = uw_sf[:]
        NC_OUTPUT.variables['vw_sf'][:] = vw_sf[:]
        NC_OUTPUT.variables['thw_sf'][:] = thw_sf[:]
        NC_OUTPUT.variables['qvw_sf'][:] = qvw_sf[:]

        NC_OUTPUT.close()

        if hid == 23:
            break

    if hid == 23:
        break

