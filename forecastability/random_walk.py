from utilities.std_imports import *
import random 

def random_walk_1D(nSteps): 
   x = 0
   y = 0
   xpos = [0]
   ypos = [0] 
   for i in range (1, nSteps+1):
       step = np.random.uniform(0,1)
       if step < 0.5: 
           x += 1
           y += 1  
       if step > 0.5: 
           x += 1
           y += -1 
 
       xpos.append(x)
       ypos.append(y)
   return xpos,ypos


def random_walk_2D(nSteps):
    x = np.zeros(nSteps) 
    y = np.zeros(nSteps) 
    direction=['up', 'down', 'right', 'left'] 

    for i in range(1, nSteps): 
        step = random.choice(direction)
        if step == 'right': 
            x[i] = x[i - 1] + 1
            y[i] = y[i - 1] 
        elif step == 'left': 
            x[i] = x[i - 1] - 1
            y[i] = y[i - 1] 
        elif step == 'up': 
            x[i] = x[i - 1] 
            y[i] = y[i - 1] + 1
        elif step == 'down': 
            x[i] = x[i - 1] 
            y[i] = y[i - 1] - 1
    return x, y


def random_walk_3D(nSteps):
    r = (np.random.rand(nSteps)*6).astype("int") 
    x = np.zeros(nSteps) 
    y = np.zeros(nSteps)
    z = np.zeros(nSteps)

    #assigning the axis for each variable 
    x[ r==0 ] = -1; x[ r==1 ] = 1 
    y[ r==2 ] = -1; y[ r==3 ] = 1
    z[ r==4 ] = -1; z[ r==5 ] = 1

    #The cumsum() : cumulative sum over a DataFrame or Series axis i.e. it sums the steps across for eachaxis of the plane
    x = np.cumsum(x) 
    y = np.cumsum(y)
    z = np.cumsum(z)
    return x,y,z