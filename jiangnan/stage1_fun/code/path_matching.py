# 功能：平行线段配对 + 提取游览中线

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

import math
from geometry import polyline_length, points_centroid

#====================== 配对阈值配置======================
ANGEL_THRESHOLD=15  # 角度阈值，单位：度
MIN_ROAD_WIDTH=1.0  # 道路最小宽度，单位：米
MAX_ROAD_WIDTH=3.0  # 道路最大宽度，单位：米
LEN_RATIO_THRESHOLD=1.5  # 两条线段最大长度比
#========================================================

def line_features(points):
    """
    计算单条线段的几何特征
    返回：方向向量、长度、中点、起点、终点
    """
    length=polyline_length(points)
    centroid=points_centroid(points)
    start=points[0]
    end=points[-1]


    # 整体方向向量（起点→终点）
    direction=(end[0]-start[0], end[1]-start[1])

    # 方向向量归一化，方便计算夹角
    dir_len=math.sqrt(direction[0]**2+direction[1]**2)
    if dir_len>0:
        direction_norm=(direction[0]/dir_len, direction[1]/dir_len)
    else:
        direction_norm=(0,0)

    return {
        'points':points,
        'length':length,
        'centroid':centroid,
        'direction_norm':direction_norm,
        'start':start,
        'end':end
    }



def angle_between_dirs(dir1,dir2):
    """计算两个归一化方向向量的夹角，单位：度，范围0~180"""
    dot=dir1[0]*dir2[0]+dir1[1]*dir2[1]
    # 限制dot在[-1,1]范围内，避免数值误
    dot=max(-1.0,min(1.0,dot))
    angle_rad=math.acos(dot)    
    return math.degrees(angle_rad)


def is_parallel_pair(feat1,feat2):

    """判断两条线段是否满足配对三条件"""
    # 条件1：平行（同向或反向都算）
    angle=angle_between_dirs(feat1['direction_norm'],feat2['direction_norm'])
    is_parallel=(angle<ANGEL_THRESHOLD or abs(angle-180)<ANGEL_THRESHOLD)
    if not is_parallel:
        return False


    # 条件2：中点距离在道路宽度范围内
    cx1,cy1=feat1['centroid']
    cx2,cy2=feat2['centroid']
    dist=math.sqrt((cx1-cx2)**2+(cy1-cy2)**2)
    if not (MIN_ROAD_WIDTH<=dist<=MAX_ROAD_WIDTH):
        return False

    
    # 条件3：长度差异不大
    len1=feat1['length']
    len2=feat2['length']
    if min(len1,len2)==0:
        return False
    ratio=max(len1,len2)/min(len1,len2)
    if ratio>LEN_RATIO_THRESHOLD:
        return False

    return True


def reverse_line(points):
    """反转一条线段的点顺序"""
    return points[::-1]

def extract_centerline(feat1,feat2):
    """
    从配对的两条边界提取中线
    先对齐方向，再对应点取中点
    """
    points1=feat1['points']
    points2=feat2['points']

    # 如果是反向平行，把第二条线反转，保证点序一致
    angle=angle_between_dirs(feat1['direction_norm'],feat2['direction_norm'])
    if abs(angle-180)<ANGEL_THRESHOLD:
        # 反向，反转其中一条线段
        points2=reverse_line(points2)

    # 以点数少的为准，一一对应取中点
    n=min(len(points1),len(points2))
    center=[]
    for i in range(n):
        x1,y1=points1[i]
        x2,y2=points2[i]
        cx=(x1+x2)/2
        cy=(y1+y2)/2
        center.append((cx,cy))

    return center

def match_and_get_centerlines(road_segments):
    """
    主函数：输入所有道路边界线段，输出真实游览中线列表
    """
    # 1. 计算所有线段的特征
    features=[]
    for seg in road_segments:
        if len(seg)<2:
            continue
        features.append(line_features(seg))

    n=len(features)
    used=[False]*n  # 标记哪些线段已经配对过
    centerlines=[]  # 存放提取出的中线

    # 2. 收集所有满足条件的配对，按距离从近到远排序
    pairs=[]
    for i in range(n):
        for j in range(i+1,n):
            if is_parallel_pair(features[i],features[j]):
                # 计算中点距离，作为排序依据
                cx1,cy1=features[i]['centroid']
                cx2,cy2=features[j]['centroid']
                dist=math.sqrt((cx1-cx2)**2+(cy1-cy2)**2)
                pairs.append((dist,i,j))

    pairs.sort()  # 距离近的优先配对

    # 3. 贪心配对，每条线只配一次
    for dist,i,j in pairs:
        if not used[i] and not used[j]:
            # 提取中线
            center=extract_centerline(features[i],features[j])
            if len(center)>=2:
                centerlines.append(center)           
            used[i]=True
            used[j]=True

    # 4. 无法配对的孤立线段（断头路、小径）直接保留
    for i in range(n):
        if not used[i]:
            centerlines.append(features[i]['points'])

    return centerlines