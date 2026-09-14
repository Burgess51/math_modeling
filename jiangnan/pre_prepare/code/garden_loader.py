# 加载单个园林的全部数据
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))

import pandas as pd
from data_parser import parse_segment_column,parse_point_column,parse_plants


def load_one_garden(excel_path):
    """
    输入：园林Excel文件路径
    输出：结构化的园林数据字典
    """

    #打开excel文件
    xls=pd.ExcelFile(excel_path)

    garden={} # 存放园林数据的字典，存整个园林的数据

    # --------------------------
    # 5类线性元素：建筑、道路、山石、水体
    # --------------------------
    # 配置：元素名称 → 是否是闭合边界
    element_config={
        '半开放建筑':True,
        '实体建筑':True,
        '道路':False,
        '假山':True,
        '水体':True
    }

    for name,is_closed in element_config.items():
        # 读取对应工作表，不要表头
        df=pd.read_excel(xls, sheet_name=name, header=0)
        # 第1列：区分线段
        segments=parse_segment_column(df.iloc[:,0], is_closed)
        # 第2列：不区分线段
        points=parse_point_column(df.iloc[:,1])
        # 存进字典
        garden[name] = {
            'segments': segments,   # 分线段 → 算长度、曲折度用
              'points': points}     # 散点 → 算面积、聚集度用

    # --------------------------
    # 植物单独处理
    # --------------------------
    df_plant=pd.read_excel(xls, sheet_name='植物', header=0)
    plants=parse_plants(df_plant.iloc[:,0],df_plant.iloc[:,1])
    garden['植物']=plants


    return garden


