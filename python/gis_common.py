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

#example 4
height = 512
width = 256

rect_pts = [[0.0, 478.9081818186243], [256.0, 500.5941322324535], [0, 512], [256, 512]]#点是无序的
rect_poly = Polygon(rect_pts)
#print(rect_poly.area)#0，#无序点导致多边形是个十字叉，面积为0
#print(dir(rect_poly))
print(rect_poly.convex_hull.area)#求多边形的最小外接矩形对应的多边形的面积

#example 5 线切开多边形
from shapely.geometry import LineString, Polygon

polygon = Polygon([[0, 512], [0, 0], [256, 0], [256, 512]])
line1 = LineString([(0, 0), (256, 512)])

line1_pol = line1.buffer(1e-3)#感觉类似于将线膨胀了一点点，变成多边形

new_polygon = polygon.difference(line1_pol)#多边形求差集
print(polygon,line1,line1_pol,new_polygon)
