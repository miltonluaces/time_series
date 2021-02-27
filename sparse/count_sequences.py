


def zero_runs(ts):
    runs = []
    run_size = 0
    for i in range(len(ts)):
        if ts[i]==0:
            run_size += 1
        if run_size>0 and ts[i]!=0:
            runs.append(run_size)
            run_size = 0
        if i==len(ts)-1 and run_size>0:
            runs.append(run_size)
    return runs


def nonzero_runs(ts):
    runs = []
    run_size = 0
    for i in range(len(ts)):
        if ts[i]!=0:
            run_size += 1
        if run_size>0 and ts[i]==0:
            runs.append(run_size)
            run_size = 0
        if i==len(ts)-1 and run_size>0:
            runs.append(run_size)
    return runs


