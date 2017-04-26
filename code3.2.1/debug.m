load('wxygt.mat');
load('wxydt.mat');
load('wxygtr.mat');
load('wxydtr.mat');
[wxygtr2,wxydtr2] = bbGt('evalRes',wxygt,wxydt,0.5);
wxygtr2
wxydtr2
