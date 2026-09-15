# 功能：转折点、交叉点识别
import math

def angle_of_vectors(v1, v2):
    """计算两个平面向量的夹角，单位：度"""
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    cross_product = v1[0] * v2[1] - v1[1] * v2[0]
    # atan2求夹角，范围0~180度
    angle_rad = math.atan2(abs(cross_product), dot_product)
    return math.degrees(angle_rad)


def find_turns_on_line(polyline,angle_threshold=30):
    """
    识别一条折线上的转折点
    angle_threshold：偏转超过多少度算转折点，默认30度
    返回：转折点坐标列表
    """
    turn_points=[]
    if len(polyline)<3:
        return turn_points  # 少于3个点无法形成转折

    #遍历中间每个点（首尾不是转折点）
    for i in range(1,len(polyline)-1):
        # 前一段方向向量
        v_before=(
            polyline[i][0]-polyline[i-1][0],
            polyline[i][1]-polyline[i-1][1]
        )
        # 后一段方向向量
        v_after=(
            polyline[i+1][0]-polyline[i][0],
            polyline[i+1][1]-polyline[i][1]
        )
        # 计算偏转角度
        turn_angle=angle_of_vectors(v_before,v_after)
        if turn_angle>angle_threshold:
            turn_points.append(polyline[i])

    return turn_points

def ccw(A,B,C):
    """辅助函数：判断三点是否逆时针排列"""
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def is_segments_intersect(p1,p2,p3,p4):
    """判断两条线段p1p2 和 p3p4 是否相交（跨立实验）"""
    A,B,C,D=p1,p2,p3,p4
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def find_all_intersections(centerlines):
    """识别所有中线之间的交叉点（岔路口）"""
    intersections=[]
    line_count=len(centerlines)

    # 两两检查所有中线对
    for i in range(line_count):
        for j in range(i+1,line_count):
            line1=centerlines[i]
            line2=centerlines[j]
            # 遍历两条线的每一小段
            for a in range(len(line1)-1):
                for b in range(len(line2)-1):
                    seg1_start=line1[a]
                    seg1_end=line1[a+1]
                    seg2_start=line2[b]
                    seg2_end=line2[b+1]

                    if is_segments_intersect(seg1_start, seg1_end, seg2_start, seg2_end):
                        # 四点平均作为交点坐标
                        ix = (seg1_start[0] + seg1_end[0] + seg2_start[0] + seg2_end[0]) / 4
                        iy = (seg1_start[1] + seg1_end[1] + seg2_start[1] + seg2_end[1]) / 4
                        intersections.append((ix, iy))

    return intersections
    




