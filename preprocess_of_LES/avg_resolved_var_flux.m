% get resolved turbulent fluxes (uw vw thw qvw; resolved)
% and resolved variables (U V W TH Q Qc; resolved)

input_path = '/intrp/';
output_path = '/avg_data/';

avg_scale = 20;

for hid = 14:23
  for mid = 0:5

    if hid == 19 && mid == 3
      continue
    end

    % read in interpolated high resolution variables for resolved variable calculations
    time = [num2str(hid),':',num2str(mid),'0:00'];
    u = ncread([input_path,'u_',time,'_intrp.nc'],'u');
    v = ncread([input_path,'v_',time,'_intrp.nc'],'v');
    w = ncread([input_path,'w_',time,'_intrp.nc'],'w');
    th = ncread([input_path,'th_',time,'_intrp.nc'],'th');
    qv = ncread([input_path,'qv_',time,'_intrp.nc'],'qv');
    qc = ncread([input_path,'qc_',time,'_intrp.nc'],'qc');

    % get domain size
    domain_size = size(u);
    nx = floor(domain_size(1)/avg_scale);
    ny = floor(domain_size(2)/avg_scale);
    nz = domain_size(3);
	
    % for saving of averaged variables
    u_avg = zeros(nx,ny,nz);
    v_avg = zeros(nx,ny,nz);
    w_avg = zeros(nx,ny,nz);
    th_avg = zeros(nx,ny,nz);
    qv_avg = zeros(nx,ny,nz);
    qc_avg = zeros(nx,ny,nz);
	
    % intermediate variable for resolved flux calculation
    u_small = zeros(avg_scale,avg_scale,nz);
    v_small = zeros(avg_scale,avg_scale,nz);
    w_small = zeros(avg_scale,avg_scale,nz);
    th_small = zeros(avg_scale,avg_scale,nz);
    qv_small = zeros(avg_scale,avg_scale,nz);
    
    % for saving of resolved fluxes
    uw = zeros(nx,ny,nz);
    vw = zeros(nx,ny,nz);
    thw = zeros(nx,ny,nz);
    qvw = zeros(nx,ny,nz);
	
    for i = 1:nx
      for j = 1:ny
        
        % calculate resolved variables
	u_avg(i,j,:) = mean(mean(u((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        v_avg(i,j,:) = mean(mean(v((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        w_avg(i,j,:) = mean(mean(w((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        th_avg(i,j,:) = mean(mean(th((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        qv_avg(i,j,:) = mean(mean(qv((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        qc_avg(i,j,:) = mean(mean(qc((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
		
        % calculate dot product in a square zone of side length n between perturbances of w and u v th q respectively
        for k = 1:nz
          u_small(:,:,k) = u((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,k) - u_avg(i,j,k);
          v_small(:,:,k) = v((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,k) - v_avg(i,j,k);
          w_small(:,:,k) = w((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,k) - w_avg(i,j,k);
          th_small(:,:,k) = th((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,k) - th_avg(i,j,k);
          qv_small(:,:,k) = qv((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,k) - qv_avg(i,j,k);
	end
        uw(i,j,:) = mean(mean(u_small.*w_small));
        vw(i,j,:) = mean(mean(v_small.*w_small));
        thw(i,j,:) = mean(mean(th_small.*w_small));
        qvw(i,j,:) = mean(mean(qv_small.*w_small));

      end
    end
	
    % write the resolved variables and turbulent fluxes to hard disk
    nccreate([output_path,'avg_turflux_',time,'.nc'],'uw','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_turflux_',time,'.nc'],'vw','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_turflux_',time,'.nc'],'thw','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_turflux_',time,'.nc'],'qvw','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'u','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'v','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'w','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'th','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'qv','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_large_',time,'.nc'],'qc','Dimensions',{'west_east',nx,'south_north',ny,'bottom_up',nz},'Datatype','single')

    ncwrite([output_path,'avg_turflux_',time,'.nc'],'uw',uw)
    ncwrite([output_path,'avg_turflux_',time,'.nc'],'vw',vw)
    ncwrite([output_path,'avg_turflux_',time,'.nc'],'thw',thw)
    ncwrite([output_path,'avg_turflux_',time,'.nc'],'qvw',qvw)
    ncwrite([output_path,'avg_large_',time,'.nc'],'u',u_avg)
    ncwrite([output_path,'avg_large_',time,'.nc'],'v',v_avg)
    ncwrite([output_path,'avg_large_',time,'.nc'],'w',w_avg)
    ncwrite([output_path,'avg_large_',time,'.nc'],'th',th_avg)
    ncwrite([output_path,'avg_large_',time,'.nc'],'qv',qv_avg)
    ncwrite([output_path,'avg_large_',time,'.nc'],'qc',qc_avg)
	
    disp(['Task ',time,' is finished'])

    if hid == 23
        break
  
  end

  if hid == 23
      break

end
