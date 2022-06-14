% get sugrid scale fluxes and add to the resolved fluxes

avg_scale = 20;
eta_path = '/intrp/';
output_path = '/avg_data/';

% height list of 14 levels in BL (0 is added in the first)
intrp_h = [0,50,100,142,192,251,319,387,474,560,665,780,906,1042,1198];

% cycling in time from 14:00:00 to 23:00:00
% 19:30:00 is skipped
for hid = 14:23
  for mid = 0:5
    
    if hid == 19 && mid == 3
      continue
    end

    time = [num2str(hid),':',num2str(mid),'0:00'];
	
    % read in surface fluxes, subgrid scale tendencies interpolated to the half leves and resolved fluxes on the full levels
    sfc_uw = ncread([eta_path,'sfc_flx_',time,'.nc'],'uw_sf');
    sfc_vw = ncread([eta_path,'sfc_flx_',time,'.nc'],'vw_sf');
    sfc_thw = ncread([eta_path,'sfc_flx_',time,'.nc'],'thw_sf');
    sfc_qvw = ncread([eta_path,'sfc_flx_',time,'.nc'],'qw_sf');
    sgs_tend_u = ncread([eta_path,'sgs_tend_',time,'_intrp.nc'],'u_tend');
    sgs_tend_v = ncread([eta_path,'sgs_tend_',time,'_intrp.nc'],'v_tend');
    sgs_tend_th = ncread([eta_path,'sgs_tend_',time,'_intrp.nc'],'th_tend');
    sgs_tend_qv = ncread([eta_path,'sgs_tend_',time,'_intrp.nc'],'qv_tend');
    reso_flx_uw = ncread([output_path,'avg_turflux_',time,'.nc'],'uw');
    reso_flx_vw = ncread([output_path,'avg_turflux_',time,'.nc'],'vw');
    reso_flx_thw = ncread([output_path,'avg_turflux_',time,'.nc'],'thw');
    reso_flx_qvw = ncread([output_path,'avg_turflux_',time,'.nc'],'qvw');
    
    % get the level differences between levels for tendency calculations
    nz = 14;
    delta_h = zeros(1,14);
    for i = 1:nz
      delta_h(i) = intrp_h(i+1)-intrp_h(i);
    end

    domain_size = size(sfc_uw);
    nx = domain_size(1);
    ny = domain_size(2);

    % for saving of subgrid scale fluxes
    sgs_flux_uw = zeros(nx,ny,nz+1);
    sgs_flux_vw = zeros(nx,ny,nz+1);
    sgs_flux_thw = zeros(nx,ny,nz+1);
    sgs_flux_qvw = zeros(nx,ny,nz+1);
    
    % start from the surface fluxes, use trapezoidal method to infer subgrid scale fluxes in full levels
    % based on subgrid scale tendencies in half levels
    sgs_flux_uw(:,:,1) = sfc_uw(:,:);
    sgs_flux_vw(:,:,1) = sfc_vw(:,:);
    sgs_flux_thw(:,:,1) = sfc_thw(:,:);
    sgs_flux_qvw(:,:,1) = sfc_qvw(:,:);
    for k = 1:nz
      sgs_flux_uw(:,:,k+1) = sgs_flux_uw(:,:,k)-sgs_tend_u(:,:,k)*delta_h(k);
      sgs_flux_vw(:,:,k+1) = sgs_flux_vw(:,:,k)-sgs_tend_v(:,:,k)*delta_h(k);
      sgs_flux_thw(:,:,k+1) = sgs_flux_thw(:,:,k)-sgs_tend_th(:,:,k)*delta_h(k);
      sgs_flux_qvw(:,:,k+1) = sgs_flux_qvw(:,:,k)-sgs_tend_qv(:,:,k)*delta_h(k);
    end
    
    % get nx and ny of averaged variables
    nx_a = floor(domain_size(1)/avg_scale);
    ny_a = floor(domain_size(2)/avg_scale);
    
    % for saving of averaged subgrid scale turbulent fluxes
    avg_flux_uw = zeros(nx_a,ny_a,nz+1);
    avg_flux_vw = zeros(nx_a,ny_a,nz+1);
    avg_flux_thw = zeros(nx_a,ny_a,nz+1);
    avg_flux_qvw = zeros(nx_a,ny_a,nz+1);
	
    % for saving of the final averaged fluxes
    flux_all_uw = zeros(nx_a,ny_a,nz);
    flux_all_vw = zeros(nx_a,ny_a,nz);
    flux_all_thw = zeros(nx_a,ny_a,nz);
    flux_all_qvw = zeros(nx_a,ny_a,nz);
    
    % get averaged subgrid scale fluxes
    for i = 1:nx_a
      for j = 1:ny_a
        avg_flux_uw(i,j,:) = mean(mean(sgs_flux_uw((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        avg_flux_vw(i,j,:) = mean(mean(sgs_flux_vw((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        avg_flux_thw(i,j,:) = mean(mean(sgs_flux_thw((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
        avg_flux_qvw(i,j,:) = mean(mean(sgs_flux_qvw((i-1)*avg_scale+1:i*avg_scale,(j-1)*avg_scale+1:j*avg_scale,:)));
      end
    end
	
    % add averaged fluxes to the resovled fluxes to get the final fluxes
    for k = 1:nz
      flux_all_uw(:,:,k) = avg_flux_uw(:,:,k+1)+reso_flx_uw(:,:,k+1);
      flux_all_vw(:,:,k) = avg_flux_vw(:,:,k+1)+reso_flx_vw(:,:,k+1);
      flux_all_thw(:,:,k) = avg_flux_thw(:,:,k+1)+reso_flx_thw(:,:,k+1);
      flux_all_qvw(:,:,k) = avg_flux_qvw(:,:,k+1)+reso_flx_qvw(:,:,k+1);
    end
	
    % write the final fluxes to hard disk
    nccreate([output_path,'avg_flux_all_',time,'.nc'],'uw','Dimensions',{'west_east',nx_a,'south_north',ny_a,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_flux_all_',time,'.nc'],'vw','Dimensions',{'west_east',nx_a,'south_north',ny_a,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_flux_all_',time,'.nc'],'thw','Dimensions',{'west_east',nx_a,'south_north',ny_a,'bottom_up',nz},'Datatype','single')
    nccreate([output_path,'avg_flux_all_',time,'.nc'],'qvw','Dimensions',{'west_east',nx_a,'south_north',ny_a,'bottom_up',nz},'Datatype','single')

    ncwrite([output_path,'avg_flux_all_',time,'.nc'],'uw',flux_all_uw)
    ncwrite([output_path,'avg_flux_all_',time,'.nc'],'vw',flux_all_vw)
    ncwrite([output_path,'avg_flux_all_',time,'.nc'],'thw',flux_all_thw)
    ncwrite([output_path,'avg_flux_all_',time,'.nc'],'qvw',flux_all_qvw)

    disp(['Task ',time,' is finished'])
    
    if hid == 23
        break

  end
    
  if hid == 23
      break

end
