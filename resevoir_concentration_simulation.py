#~~~~
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
conc = float(input("conc(mg/l):")) #초기농도
time = int(input("time(hr):")) # 관측 시간
height = int(input("height(m):")) #저류조 높이
organic = float(input("유기물 비율(0~1):")) #유기물 비율(0~1)
non_organic = 1 - organic
name = input('파일명을 입력하시오')
v=0
d=0
a = 0
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# stokes law
K = (1/18)*9.8*(1/0.00089)*(1300*organic+2600*non_organic-1000)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 층 구분 layer_시간_깊이
for i in range(1,time+1,1):
    for j in range(1,height+1,1):
        globals()['layer_{0}_{1}'.format(i,j)] = 0
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 입자 직경에 따른 질량분율: percent_i

for i in range(30,1441,1):
    if i == 30:
        globals()['percent_{}'.format(i)]=(23.7 * math.log(i/10)-17.826)/100    
    else:        
        globals()['percent_{}'.format(i)]=(23.7 * math.log(i/10)-17.826)/100 -((23.7 * math.log((i-1)/10)-17.826)/100)
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
# 입자 크기에 따른 속도 (m/h): velocity_i
speed =[]
for i in range(30,1441,1):
    globals()['velocity_{}'.format(i)]=3600*K*i*i/100000000000000 
    #print(globals()['velocity_{}'.format(i)])
    speed.append(globals()['velocity_{}'.format(i)]) # 속도 그래프

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#distance_시간_직경 생성
count=0
for i in range(1,time+1,1):
    for j in range(30,1441,1):
        globals()['distance_{0}_{1}'.format(i,j)] = globals()['velocity_{}'.format(j)]*i
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 농도 계산
for i in range(1,time+1,1):
    for j in range(1,height+1,1):
        if j != height:
            for k in range(30,1441,1):
                if int(globals()['distance_{0}_{1}'.format(i,k)]) == j-1:
                    globals()['layer_{0}_{1}'.format(i,j)] +=conc * globals()['percent_{}'.format(k)]
                    #print(i,j)
                   
        else:
            for k in range(30,1441,1):
                if int(globals()['distance_{0}_{1}'.format(i,k)]) >= j-1:
                    globals()['layer_{0}_{1}'.format(i,j)] +=conc * globals()['percent_{}'.format(k)]
                    



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

for i in range(1,time+1,1):
    for j in range(1,height+1,1):
        globals()['layer2_{0}_{1}'.format(i,j)] = 0

                
                
for i in range(1,time+1,1):
    for j in range(1,height+1,1):
        if j != height:
            for k in range(0,j,1):
                globals()['layer2_{0}_{1}'.format(i,j)] += globals()['layer_{0}_{1}'.format(i,j-k)]            
        else:
            for k in range(0,j,1):
                globals()['layer2_{0}_{1}'.format(i,j)] += globals()['layer_{0}_{1}'.format(i,j-k)]*(j-k)
                

    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 파일 생성 과정

        
for i in range(1,height+1,1):
    globals()['depth_{}'.format(i)] = []

for i in range(1,height+1,1):
    for j in range(1,time+1,1):
        globals()['depth_{}'.format(i)].append(globals()['layer2_{0}_{1}'.format(j,i)])


depth = []
for i in range(1,height+1,1):
    depth.append(globals()['depth_{}'.format(i)],)

depth_pd = pd.DataFrame(depth)
list_a = list(range(1,time+1,1))
list_b = list(range(1,height+1,1))

#y:layer, x: time
depth_pd.columns = list_a
depth_pd.index = list_b
depth_pd.to_csv('{0}.csv'.format(name))
#print(depth_pd)