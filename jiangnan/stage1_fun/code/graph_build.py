# 功能：计算路径特征指标

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

from geometry import polyline_length
from turn_detection import find_turns_on_line, find_all_intersections

def calculate_path_metrics(centerlines, garden_area):
    """
    输入：
        centerlines：游览中线列表
        garden_area：园林总面积（平方米），用于归一化
    输出：
        metrics：路径特征指标字典
        all_turns：所有转折点坐标
        all_crosses：所有交叉点坐标
    """
    # 1. 基础统计：总长度、转折点
    total_length = 0.0
    all_turns = []
    
    for line in centerlines:
        total_length += polyline_length(line)
        line_turns = find_turns_on_line(line)
        all_turns.extend(line_turns)
    
    turn_count = len(all_turns)
    
    # 2. 统计交叉点
    all_crosses = find_all_intersections(centerlines)
    cross_count = len(all_crosses)
    
    # 3. 归一化指标（消除园林大小影响）
    path_density = total_length / garden_area if garden_area > 0 else 0
    turn_density = turn_count / total_length if total_length > 0 else 0
    cross_density = cross_count / total_length if total_length > 0 else 0
    
    # 整理结果
    metrics = {
        '总游线长度(米)': round(total_length, 2),
        '转折点数量': turn_count,
        '交叉点数量': cross_count,
        '单位面积路径密度(米/平米)': round(path_density, 6),
        '单位长度转折数(次/米)': round(turn_density, 4),
        '单位长度交叉数(次/米)': round(cross_density, 4)
    }
    
    return metrics, all_turns, all_crosses