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

box_points1 = [[0, 0], [0, 50], [50, 50], [50, 0]]
polygon1 = Polygon(box_points1)

#box_points2 = [[0, 0], [0, 100], [100, 100], [100, 0]]
#polygon2 = Polygon(box_points2)

box_points2 = [[10, 0], [40, 0], [25, 100]]
polygon2 = Polygon(box_points2)

intersection_polygon = polygon1.intersection(polygon2)
print(intersection_polygon)

#POLYGON ((0 0, 0 50, 50 50, 50 0, 0 0))
#POLYGON ((17.5 50, 32.5 50, 40 0, 10 0, 17.5 50))

#example 3,线与多边形交点
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString

height = 512
width = 256
rect_pts = [[0,0],[0,height],[width,height],[width,0]]
rect_poly = Polygon(rect_pts)

k = -1
c = 35

line = LineString([(0,c), (width,width*k+c)])
print(line)

intersection = rect_poly.intersection(line)
print(intersection)
