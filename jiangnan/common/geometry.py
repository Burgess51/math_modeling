# common/geometry.py
# 基础几何计算工具，所有阶段共用

import math

def polyline_length(points):
    """
    计算一条折线的总长度
    输入：points = [(x1,y1), (x2,y2), ...] 一串点
    输出：总长度（米）
    """
    total=0.0
    # 遍历每一段线段，计算长度并累加
    for i in range(len(points)-1):
        x1,y1=points[i]
        x2,y2=points[i+1]
        dx=x2-x1
        dy=y2-y1
        # 勾股定理算两点距离
        distance=math.sqrt(dx*dx+dy*dy)
        total+=distance
    return total


def polygon_area(points):
    """
    鞋带公式：计算闭合多边形的面积
    要求：点按顺序排列，首尾两个点重合
    输入：多边形顶点列表
    输出：面积（平方米）
    """
    if len(points)<3:
        return 0.0  # 少于3个点无法构成多边形

    area=0.0
    n=len(points)
    for i in range(n):
        x1,y1=points[i]
        x2,y2=points[(i+1)%n]  # 下一个点，首尾相连
        area+=x1*y2-x2*y1
    return abs(area)/2.0


def point_centroid(points):
    """
    计算一组点的质心（几何中心）
    输入：points = [(x1,y1), (x2,y2), ...]
    输出：质心坐标 (cx, cy)
    """
    if not points:
        return (0.0, 0.0)  # 空点集返回原点

    sum_x=0.0
    sum_y=0.0
    for x,y in points:
        sum_x+=x
        sum_y+=y

    # 平均值就是质心
    cx=sum_x/len(points)
    cy=sum_y/len(points)
    return (cx, cy)

