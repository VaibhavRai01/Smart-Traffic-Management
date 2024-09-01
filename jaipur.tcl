# set number of nodes
set opt(nn) 100

# set activity file
set opt(af) $opt(config-path)
append opt(af) /activity.tcl

# set mobility file
set opt(mf) $opt(config-path)
append opt(mf) /mobility.tcl

# set start/stop time
set opt(start) 0.0
set opt(stop) 100.00000000000001

# set floor size
set opt(x) 1265.34
set opt(y) 1113.52
set opt(min-x) 104.28
set opt(min-y) 0.12

