Fig. 1. Game map.
![alt text](E:\programming\python\projects\strategy\notes\fig1.png)

Fig. 2. Start, end, and grid_str output.
```
start: (7, 0), image_map_object_mountain_1.png
end: (6, 2), image_map_object_mountain_1.png
path: [(7, 0), (7, 1), (7, 2), (6, 2)], runs: 4
+--------+
|#  ####s|
|#  ####x|
|#     ex|
|#     # |
|###     |
|##    # |
|###   ##|
|      ##|
+--------+
```

We can see that:
1. grid_str output roughly matches the map screen: it looks all OK at the first glance. The "pattern" is here, but! It starts from the corner that is empty, does not contain any MapObject.
2. Arcade starting point (0, 0) is located, I believe, in the bottom-left corner. Why finder starts from the top-right corner, if coords of MapObject are (7, 0)? Looks like the coordinates of MapObject are wrong? (7, 0) should be placed on the bottom-right corner.

Another example of wrongly placed start tile. There is no visible object in the "start" place.
Fig. 3.
![alt text](E:\programming\python\projects\strategy\notes\fig3.png)
Fig. 4.
```
start: (3, 0), image_map_object_mountain_1.png
end: (4, 3), image_map_object_mountain_1.png
path: [], runs: 41
+--------+
|#  s    |
|#     # |
|# #     |
|# # e# #|
|#   ##  |
|##  ##  |
|#   ## #|
|   #   #|
+--------+
```


Number of MapObject instances per map does match:

Fig. 5.
![alt text](E:\programming\python\projects\strategy\notes\fig5.png)

Fig. 6.
```
len(self.grid.map_objects.objects): 23
```

And the positioning of cities seems correct, too:
```
x: 0, y: 1, name: image_map_object_city_1.png
x: 6, y: 1, name: image_map_object_city_1.png
x: 6, y: 5, name: image_map_object_city_1.png
x: 3, y: 7, name: image_map_object_city_1.png
x: 0, y: 3, name: image_map_object_city_1.png
```

It looks like I should invert matrix?

