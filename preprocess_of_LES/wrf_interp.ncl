load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

nx = 2000
ny = 2000
nz = 14

; this is the height list for the interpolation of variables to the specific height

; Large scale variables (u v w th qv qc) are interpolated to the full levels, so you use intrp_h.

; Subgrid scale tendencies (u_tend v_tend th_tend qv_tend) are interpolated to the half levels for
; further calculations of subgrid scale fluxes in surface layer, so you use intrp_hh this time

intrp_h = (/50,100,142,192,251,319,387,474,560,665,780,906,1042,1198/)
;intrp_hh = (/25,50,121,167,221.5,285,353,430.5,517,612.5,722.5,843,974,1120/)

input_path = "/tc_les/"
output_path = "/intrp/"

; circling for all the time stamp of LES output
; circle from 14:00:00 to 23:00:00. 19:30:00 is skipped because this data is broken
do hid = 14,23
    do mid = 0,5
        if ((hid .eq. 19).and. (mid .eq. 3))
            continue
        end if
        
        ; read in netcdf file of TC-LES
        f = addfile(input_path+"wrfout_d04_2007-09-05_"+hid+":"+mid+"0:00","r")
        
        ;read in variables
        z = wrf_user_getvar(f,"z",0)
        u = wrf_user_getvar(f,"ua",0)
        v = wrf_user_getvar(f,"va",0)
        w = wrf_user_getvar(f,"wa",0)
        u_tend = wrf_user_getvar(f,"U_TEND",0)
        v_tend = wrf_user_getvar(f,"V_TEND",0)
        th_tend = wrf_user_getvar(f,"TH_TEND",0)
        qv_tend = wrf_user_getvar(f,"Q_TEND",0)
        th = wrf_user_getvar(f,"th",0)
        qv = wrf_user_getvar(f,"QVAPOR",0)
        qc = wrf_user_getvar(f,"QCLOUD",0)
        
        ; for saving interpolated variables
        u_output = new((/nz,ny,nx/),float)
        v_output = new((/nz,ny,nx/),float)
        w_output = new((/nz,ny,nx/),float)
        u_tend_output = new((/nz,ny,nx/),float)
        v_tend_output = new((/nz,ny,nx/),float)
        th_tend_output = new((/nz,ny,nx/),float)
        qv_tend_output = new((/nz,ny,nx/),float)
        th_output = new((/nz,ny,nx/),float)
        qv_output = new((/nz,ny,nx/),float)
        qc_output = new((/nz,ny,nx/),float)

        ; output files
        u_hf = addfile(path+"u_"+hid+":"+mid+"0:00_intrp.nc","c")
        v_hf = addfile(path+"v_"+hid+":"+mid+"0:00_intrp.nc","c")
        w_hf = addfile(path+"w_"+hid+":"+mid+"0:00_intrp.nc","c")
        u_tend_hf = addfile(output_path+"u_tend_"+hid+":"+mid+"0:00_intrp.nc","c")
        v_tend_hf = addfile(output_path+"v_tend_"+hid+":"+mid+"0:00_intrp.nc","c")
        th_hf = addfile(output_path+"th_"+hid+":"+mid+"0:00_intrp.nc","c")
        qv_hf = addfile(output_path+"qv_"+hid+":"+mid+"0:00_intrp.nc","c")
        sgs_tend_hf = addfile(output_path+"sgs_tend_"+hid+":"+mid+"0:00_intrp.nc","c")
        qc_hf = addfile(output_path+"qc_"+hid+":"+mid+"0:00_intrp.nc","c")

        ; interpolation of variables on full levels or half levels
        do level = 0,nz-1
            h = intrp_h(level)  ; use intrp_h or intrp_hh for different variables as mentioned before
            u_h = wrf_user_intrp3d(u,z,"h",h,0.,False)
            v_h = wrf_user_intrp3d(v,z,"h",h,0.,False)
            w_h = wrf_user_intrp3d(w,z,"h",h,0.,False)
            u_output(level,:,:) = u_h(:,:)
            v_output(level,:,:) = v_h(:,:)
            w_output(level,:,:) = w_h(:,:)
            u_tend_h = wrf_user_intrp3d(u_tend,z,"h",h,0.,False)
            v_tend_h = wrf_user_intrp3d(v_tend,z,"h",h,0.,False)
            th_tend_h = wrf_user_intrp3d(th_tend,z,"h",h,0.,False)
            qv_tend_h = wrf_user_intrp3d(qv_tend,z,"h",h,0.,False)
            u_tend_output(level,:,:) = u_tend_h(:,:)
            v_tend_output(level,:,:) = v_tend_h(:,:)
            th_tend_output(level,:,:) = th_tend_h(:,:)
            qv_tend_output(level,:,:) = qv_tend_h(:,:)
            th_h = wrf_user_intrp3d(th,z,"h",h,0.,False)
            th_output(level,:,:) = th_h(:,:)
            qv_h = wrf_user_intrp3d(qv,z,"h",h,0.,False)
            qv_output(level,:,:) = qv_h(:,:)
            qc_h = wrf_user_intrp3d(qc,z,"h",h,0.,False)
            qc_output(level,:,:) = qc_h(:,:)
        end do

        ; write the interpolated file to the hard disk
        u_hf->u = u_output
        v_hf->v = v_output
        w_hf->w = w_output
        u_tend_hf->u_tend = u_tend_output
        v_tend_hf->v_tend = v_tend_output
        th_hf->th = th_output
        qv_hf->qv = qv_output
        sgs_tend_hf->u_tend = u_tend_output
        sgs_tend_hf->v_tend = v_tend_output
        sgs_tend_hf->th_tend = th_tend_output
        sgs_tend_hf->qv_tend = qv_tend_output
        qc_hf->qc = qc_output

        print("Task "+hid+":"+mid+"0:00 is finished")
    
        if (hid .eq. 23)
            break
        end if

    end do
    
    if (hid .eq. 23)
        break
    end if

end do
