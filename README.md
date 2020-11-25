# DTN

### Usage
```
python DataGenerator.py
       --width          # width of the region, default = 15000
       --height         # height of the region, default = 15000
       --routes_num     # number of routes, default = 5
       --cars_num       # number of cars, default = 15
       --base_speed     # explain below, default = 10
       --speed_noise    # explain below, default = 1
       --stage_num      # number of stages, default = 3
       --stage_time     # time of each stage, default = 1800
       --drawOnlyRoutes # draw the pic only with current routes or not, default = False
       --reassign       # re-assign the route to each car after each stage or not, default = True
       --speedwNoise    # set different speed for different blocks, default = True
```

### Current settings

#### Block
```
789
456
123
```
將現有區域平均切割成九個區塊，編號規則如上，在參數 speedwNoise 設定為 True 的情況下，\
各區塊的速度如下:\
區塊 1, 3, 7, 9: base_speed + speed_noise \
區塊 2, 4, 6, 8: base_speed \
區塊 5: base_speed - speed_noise

#### Stage
每一階段結束後，假使 reassign 為 True，每台車輛將會被分配到不同的路線。\
速度會在 9~11 之間隨機選擇一個速度，noise 會在 0~2 之間隨機選擇。 \
(TODO: 速度將在 base_speed-x ~ base_speed+x 之間隨機選擇)

#### Route
會在 9 個 block 當中隨機選擇 routes_num 個 block (Not sure what will happen if routes_num > 9)\
在每個 block 的中心附近選擇一個點作為該條路線的左下角(x0,y0)，其他座標順時鐘旋轉依序為 (x1, y1), (x2, y2), (x3, y3)\
路線的長寬也會隨機生成，假使超過邊界，就以到邊界的距離做為長寬。\
初始路線時會隨機決定順時針或逆時針旋轉，所有在此路線上的車輛都會依此去跑。
