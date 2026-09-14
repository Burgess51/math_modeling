# 数据清洗模块：修复原始数据的各种缺陷
'''
专门修复原始数据的缺陷，对应题目要求的「数据可能存在不完整，需合理处理」。
一共 4 步清洗：去重 → 剔异常 → 闭合修正 → 过滤碎线。
'''
import sys
import os
# 把common文件夹加入路径，才能导入公共工具
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

import math
from config import MIN_SEGMENT_LENGTH, SIGMA_TIMES
from geometry import polyline_length, point_centroid

def clean_single_segment(points, is_closed=False):
    """
    清洗单条线段的点集
    参数：
        points：原始点列表 [(x1,y1), (x2,y2)...]
        is_closed：是否是闭合边界（建筑/水体/山石=True，道路=False）
    返回：清洗后的点列表；无效就返回空列表
    """
    # --------------------------
    # 第1步：相邻去重
    # 去掉连续重复的点（采样冗余导致的）
    # --------------------------
    new_points=[]
    for p in points:
        # 和上一个点不一样，才保留
        if len(new_points)==0 or p!=new_points[-1]:
            new_points.append(p)
    points=new_points

    # 少于2个点的线段没用，直接返回空
    if len(points)<2:
        return []

    # --------------------------
    # 第2步：3σ原则剔除离群异常点
    # 偏离整体太远的点，大概率是脏数据
    # --------------------------
    cx,cy=point_centroid(points)
    # 计算所有点到质心的距离
    dists=[]
    for x,y in points:
        d=math.sqrt((x-cx)**2+(y-cy)**2)
        dists.append(d)

    # 算距离的平均值和标准差
    mean_d=sum(dists)/len(dists)
    std_d=math.sqrt(sum((d-mean_d)**2 for d in dists)/len(dists))

    # 只保留「平均值±3倍标准差」范围内的点
    if std_d > 0.000001:# 防止所有点重合，标准差为0
        filtered=[]
        for i in range(len(points)):
            if abs(dists[i]-mean_d)<=SIGMA_TIMES*std_d:
                filtered.append(points[i])
        points=filtered

    if len(points)<2:
        return []

    # --------------------------
    # 第3步：闭合修正
    # 建筑、湖岸这些闭合边界，强制首尾点一样
    # --------------------------
    if is_closed and len(points)>=3:
        if points[0]!=points[-1]:
            points.append(points[0])    # 把第一个点补到最后

    # --------------------------
    # 第4步：过滤过短的碎线段
    # 小于1米的碎线，是绘图残留，直接丢掉
    # --------------------------
    if polyline_length(points)<MIN_SEGMENT_LENGTH:
        return []

    return points
