#求两个多边行的交集（也是一个多边形）的面积
from shapely.geometry import box,Polygon
xy = [[0.0, 0], [0, 100], [100, 100], [100, 0]]
polygon_shape = Polygon(xy)

xy = [[0.0, 0], [0, 50], [50, 50], [50, 0]]
polygon_shape2 = Polygon(xy)

gridcell_shape = box(0, 0, 50, 50)

#print(polygon_shape.intersection(polygon_shape2))
#print(polygon_shape.intersection(polygon_shape2).area)
#POLYGON ((0 0, 0 50, 50 50, 50 0, 0 0))
#2500.0

print(polygon_shape.intersection(gridcell_shape))
print(polygon_shape.intersection(gridcell_shape).area)
#POLYGON ((0 0, 0 50, 50 50, 50 0, 0 0))
#2500.0
