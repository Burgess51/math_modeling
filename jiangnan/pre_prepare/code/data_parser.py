# 解析Excel里的字符串坐标

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

import re
from config import MM_TO_M,MAX_PLANT_RADIUS
from data_cleaner import clean_single_segment


#`parse_one_cell` 是最小单位，一个单元格一个单元格地认
def parse_one_cell(cell_str):
    """
    解析单个单元格的字符串
    返回三种可能：
    1. ('segment', 线段编号) → 遇到了线段开头标记
    2. ('point', (x, y))     → 遇到了坐标点，单位米
    3. None                 → 无效内容
    """
    cell_str=str(cell_str).strip()  # 转成字符串，去掉首尾空格

    # 匹配线段标记：格式是 {0; 数字}
    seg_match=re.match(r'\{0;\s*(\d+)\}', cell_str)
    if seg_match:
        seg_id=int(seg_match.group(1))  # 提取线段编号
        return ('segment', seg_id)

    # 匹配坐标点：格式是 {x, y, 0}
    point_match=re.match(r'\{-?\d+(\.\d+)?,\s*(-?\d+(\.\d+)?),\s*0\}', cell_str)
    if point_match:
        x=float(point_match.group(1))*MM_TO_M  # 转成米
        y=float(point_match.group(2))*MM_TO_M
        return ('point', (x, y))

    # 都匹配不上就是无效内容
    return None


def parse_segment_column(column_data, is_closed=False):
    """
    解析「区分线段点位」的一列数据（Excel第1列）
    返回：线段列表，每个元素是一条线段的点列表
    """
    all_segments=[] # 存所有线段
    current_points=[]   # 存当前正在攒的一条线段的点

    for cell in column_data:
        result=parse_one_cell(cell)
        if result is None:
            continue  # 无效内容，跳过

        typ,val=result

        if typ=='segment':
            # 遇到线段开头标记，说明上一条线段结束了→ 把上一条线段清洗后存起来
            if len(current_points)>0:
                # 清洗当前线段的点集
                cleaned=clean_single_segment(current_points, is_closed)
                if len(cleaned)>0:
                    all_segments.append(cleaned)
                current_points=[]  # 清空，准备攒下一条线段
        elif typ=='point':
            # 遇到坐标点，加入当前线段的点集
            current_points.append(val)


    # 循环结束后，最后一条线段也要处理
    if len(current_points)>0:
        cleaned=clean_single_segment(current_points, is_closed)
        if len(cleaned)>0:
            all_segments.append(cleaned)

    return all_segments


def parse_point_column(column_data):
    """
    解析「不区分线段点位」的一列数据（Excel第2列）
    返回：所有点平铺成一个大列表
    """
    all_points=[]

    for cell in column_data:
        result=parse_one_cell(cell)
        if result is None:
            continue  # 无效内容，跳过

        typ,val=result
        if typ=='point':
            all_points.append(val)

    # 整体去重
    all_points=list(set(all_points))
    return all_points

def parse_plants(center_col,radius_col):
    """
    解析植物数据
    返回：列表，每个元素是 (x, y, 冠径半径) 单位：米
    """
    plants=[]
    # 同时遍历两列：中心坐标列 + 冠径列
    for c,r in zip(center_col,radius_col):
        result=parse_one_cell(c)
        if result is None:
            continue  # 无效内容，跳过

        typ,(x,y)=result
        if typ!='point':   
            continue  # 不是坐标点，跳过

        try:
            radius=float(r)*MM_TO_M  # 冠径单位转成米
        except:
            continue  # 冠径不是数字，跳过

        # 过滤异常冠径
        if 0<radius<=MAX_PLANT_RADIUS:
            plants.append((x,y,radius))

    return plants
        