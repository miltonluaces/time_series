from math import sqrt
import random
from sklearn.metrics import classification_report

# Euclidean distance
def euclid_dist(ts1,ts2):
    return sqrt(sum((ts1-ts2)**2))


# DTW (Distance Time Warping)
def dtw_dist(ts1, ts2):
    DTW={}
    
    for i in range(len(ts1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(ts2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(ts1)):
        for j in range(len(ts2)):
            dist= (ts1[i] - ts2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])

    return sqrt(DTW[len(ts1)-1, len(ts2)-1])


# Weighted DTW (Distance Time Warping)
def wdtw_dist(ts1, ts2, w):
    
    DTW={}
    
    w = max(w, abs(len(ts1)-len(ts2)))
    
    for i in range(-1,len(ts1)):
        for j in range(-1,len(ts2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0
  
    for i in range(len(ts1)):
        for j in range(max(0, i-w), min(len(ts2), i+w)):
            dist= (ts1[i]-ts2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return sqrt(DTW[len(ts1)-1, len(ts2)-1])


# LB Keogh lower bound of dynamic time warping
def lbkeogh_dist(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):
        
        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        
        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2
    
    return sqrt(LB_sum)


def knn(train,test,w):
    preds=[]
    for ind,i in enumerate(test):
        min_dist=float('inf')
        closest_seq=[]
        #print ind
        for j in train:
            if lbkeogh_dist(i[:-1],j[:-1],5)<min_dist:
                dist=wdtw_dist(i[:-1],j[:-1],w)
                if dist<min_dist:
                    min_dist=dist
                    closest_seq=j
        preds.append(closest_seq[-1])
    return classification_report(test[:,-1],preds)


def k_means_clust(data, num_clust, num_iter, w=5):
    centroids=random.sample(data,num_clust)
    counter=0
    for n in range(num_iter):
        counter+=1
        print(counter)
        assignments={}
        #assign data points to clusters
        for ind,i in enumerate(data):
            min_dist=float('inf')
            closest_clust=None
            for c_ind,j in enumerate(centroids):
                if lbkeogh_dist(i,j,5)<min_dist:
                    cur_dist=wdtw_dist(i,j,w)
                    if cur_dist<min_dist:
                        min_dist=cur_dist
                        closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
    
        #recalculate centroids of clusters
        for key in assignments:
            clust_sum=0
            for k in assignments[key]:
                clust_sum=clust_sum+data[k]
            centroids[key]=[m/len(assignments[key]) for m in clust_sum]
    
    return centroids