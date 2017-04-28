function mgp(flow_root, score_root, output_root, frame_root)
temporal_window_size = 7;
half_tws = floor(temporal_window_size / 2);

video_name = dir(frame_root);
video_name = video_name(3:end);
n_frame = length(video_name);

frame = get_score(score_root, n_frame);

file = fopen(output_root,'w');

%for video_idx = 1:n_video
    %% optical flow

    neighbor_frame = struct('boxes',[],'zs',[]);
    neighbor_frame(n_frame).boxes = [];
   % neighbor_frame = frame;

%     fprintf(' Loading boxes.');
    for frame_idx = 1:n_frame
       % optflow_name = fullfile(flow_root, video_name(video_idx).name, [frame_name(frame_idx).name(1:dot_pos-1) '.png']);
        optflow_name = fullfile(flow_root,[int2str(frame_idx) '.png']);
       % frame(frame_idx) = load(file_name);
        if isempty(frame(frame_idx).boxes)
            continue;
%             frame(frame_idx).boxes = zeros(0,4);
%             frame(frame_idx).zs = zeros(0,30);
        end
        optflow = imread(optflow_name);
        x_map = single(optflow(:,:,1)) / 255 * 30 - 15;
        y_map = single(optflow(:,:,2)) / 255 * 30 - 15;
        [m,n] = size(x_map);
        box_avg_x = boxes_average_sum(x_map, frame(frame_idx).boxes);
        box_avg_y = boxes_average_sum(y_map, frame(frame_idx).boxes);

        for offset_idx = [-half_tws:-1 1:half_tws]
            neighbor_frame_idx = frame_idx + offset_idx;
            if neighbor_frame_idx < 1 || neighbor_frame_idx > n_frame
                continue;
            end

            boxes = frame(frame_idx).boxes;
            zs = frame(frame_idx).zs;
            if abs(offset_idx) >= 3
                zs(:,1) = -1e+5;
            end
            boxes = boxes + ([box_avg_x, box_avg_y, box_avg_x, box_avg_y] * offset_idx);
            boxes(:,1) = max(boxes(:,1),1);
            boxes(:,2) = max(boxes(:,2),1);
            boxes(:,3) = min(boxes(:,3),n);
            boxes(:,4) = min(boxes(:,4),m);
            neighbor_frame(neighbor_frame_idx).boxes = cat(1, neighbor_frame(neighbor_frame_idx).boxes, boxes);
            neighbor_frame(neighbor_frame_idx).zs = cat(1, neighbor_frame(neighbor_frame_idx).zs, zs);
        end
    end

    fprintf(1, ' Saving boxes.\n');
    for frame_idx = 1:n_frame
        clear boxes zs;
        boxes = cat(1, neighbor_frame(frame_idx).boxes, frame(frame_idx).boxes);
        zs = cat(1, neighbor_frame(frame_idx).zs, frame(frame_idx).zs);
        for id = 1:size(boxes,1)
            fprintf(file,'%d %f %f %f %f %f\n',frame_idx, boxes(id,1),boxes(id,2), ...
                boxes(id,3),boxes(id,4),zs(id,1));
        end
        
%         if ~isempty(zs)
%             zs(:,top_classes) = zs(:,top_classes) + top_bonus;
%         end
% 
%         output_dir = fullfile(output_root, video_name(video_idx).name);
%         mkdir_if_missing(output_dir);
%         output_path = fullfile(output_dir, frame_name(frame_idx).name);
%         save(output_path, boxes, zs);

    end
    clear frame neighbor_frame;
    fclose(file);
end


%end
function frame = get_score(score_root,n_frame)
skip = 1;
frames = skip-1:skip:n_frame-1;
bbs = load(score_root,'-ascii');
k = 0;
frame = struct('boxes',[],'zs',[]);
frame(n_frame).boxes = [];

for f=frames, bb=bbs(bbs(:,1)==f+1,:);
    k = k+1; 
    frame(k).boxes = bb(:,2:5);
    frame(k).zs = bb(:,6);
end
end