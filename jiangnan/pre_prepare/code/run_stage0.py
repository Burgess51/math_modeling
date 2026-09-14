# 阶段0：数据预处理 运行入口
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

from garden_loader import load_one_garden
from geometry import polyline_length

# ====================== 配置区 ======================
# 要处理的园林名称
GARDEN_NAME='寄畅园'
# 对应Excel文件路径
EXCEL_PATH='jiangnan/dataset/3. 寄畅园/4-寄畅园数据坐标.xlsx'
# 输出文件夹
OUTPUT_DIR='jiangnan\\pre_prepare\\output'
# ===================================================

if __name__=='__main__':
    # 确保输出文件夹存在，没有就自动建
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f'====阶段0：处理园林【{GARDEN_NAME}】')

    #1.加载并清洗数据
    garden=load_one_garden(EXCEL_PATH)

    #2.统计基础信息
    result_lines=[]
    result_lines.append(f'园林名称：{GARDEN_NAME}')
    result_lines.append('*'*30)

    #统计水体
    water_segs=garden['水体']['segments']
    water_len=sum(polyline_length(seg) for seg in water_segs)
    result_lines.append(f'水体线段总数：{len(water_segs)}')
    result_lines.append(f'水体总岸线长度：{water_len:.2f}米')

    #统计道路
    road_segs=garden['道路']['segments']
    road_len=sum(polyline_length(seg) for seg in road_segs)
    result_lines.append(f'道路线段总数：{len(road_segs)}')
    result_lines.append(f'道路总长度：{road_len:.2f}米')    

    #统计实体建筑
    build_segs=garden['实体建筑']['segments']
    result_lines.append(f'实体建筑数量：{len(build_segs)}栋')

    #统计半开放建筑
    semi_build_segs=garden['半开放建筑']['segments']    
    result_lines.append(f'半开放建筑数量：{len(semi_build_segs)}栋')

    #统计植物
    result_lines.append(f'植物数量：{len(garden["植物"])}棵')

    #3.打印到屏幕
    for line in result_lines:
        print(line)

    #4.保存结果到output文件夹
    output_file=os.path.join(OUTPUT_DIR, f'{GARDEN_NAME}_基础统计.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result_lines))

    print(f'结果已保存到：{output_file}')
    print('====阶段0：处理完成====')