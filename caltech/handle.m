ansdir = '/Volumes/X.Y.W/annotations/';
nFramedir = fullfile(ansdir, 'framesnum.txt');
setsdir = {'set06','set07','set08','set09','set10'};
idother = '000000';
mol = 30;
startFrame = 30;
wxy = fopen(nFramedir,'w');
for item = 1:length(setsdir)
    setdir = setsdir(item);
    setdir = setdir{1,1};
    tmp = fullfile(ansdir,setdir);
   % tmp = tmp{1,1};
    tmps = dir(tmp);
    for matid = 1:length(tmps)
        mat = tmps(matid);
        if mat.name(1) ~= '.'
            matname = mat.name;
            curdir = fullfile(ansdir, setdir, matname);
          %  matname = matname{1,1}
            id = strcat(setdir(4:5), matname(2:4));
            a = load(curdir);
            numframe = a.A.nFrame;
            objs = a.A.objLists;
            labs = a.A.objLbl;
            setid = str2num(setdir(4:5));
            volid = str2num(matname(2:4));
            fprintf(wxy,'%d %d %d\n', setid, volid, numframe);
            for i = startFrame:mol:numframe
                sigle = objs(1,i);
                sigle = sigle{1,1};
                len = size(sigle, 2);
                %if len ~= 0
                txtname = strcat(idother, int2str(i));
                txtname = txtname(size(txtname,2)-5:size(txtname,2));
                txtname = strcat(id, txtname);
                txtpath = fullfile(ansdir,'testtxts',strcat(txtname, '.txt'))
                f = fopen(txtpath, 'w');
                fprintf(f, 'setid: %d\n',str2num(setdir(4:5)));
                fprintf(f, 'volid: %d\n',str2num(matname(2:4)));
                fprintf(f, 'frameid: %d\n',i);
                fprintf(f, 'name: %s\n', txtname);
                fprintf(f, 'num: %d\n', len);
                for j = 1:len
                    fprintf(f, 'label: %s\n', labs{1,sigle(j).id});
                    fprintf(f, 'pos: %f %f %f %f\n', sigle(j).pos(1), sigle(j).pos(2), sigle(j).pos(3), sigle(j).pos(4));
                    fprintf(f, 'occl: %d\n', sigle(j).occl);
                    fprintf(f, 'lock: %d\n', sigle(j).lock);
                    fprintf(f, 'posv: %f %f %f %f\n', sigle(j).posv(1), sigle(j).posv(2), sigle(j).posv(3), sigle(j).posv(4));
                end
                    fclose(f);
                   
                    %  end
            end
        end
    end  
end
fclose(wxy);



