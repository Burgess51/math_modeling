import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../pre_prepare/code'))

from garden_loader import load_one_garden
from path_matching import match_and_get_centerlines
from graph_build import calculate_path_metrics

# ====================== 配置区 ======================
GARDEN_NAME = '寄畅园'
EXCEL_PATH = 'jiangnan/dataset/3. 寄畅园/4-寄畅园数据坐标.xlsx'
GARDEN_AREA = 10000.0  # 园林总面积，单位：平方米（寄畅园约1.0万m²）
OUTPUT_DIR = 'jiangnan\\stage1_fun\\output'
# ===================================================

if __name__ == '__main__':
    # 自动创建输出文件夹
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"===== 问题1-1：路径刻画【{GARDEN_NAME}】 =====")
    
    # 1. 加载原始道路边界数据（复用阶段0的加载器）
    garden = load_one_garden(EXCEL_PATH)
    road_segments = garden['道路']['segments']
    print(f"原始道路边界线段数：{len(road_segments)}")
    
    # 2. 平行配对 + 提取游览中线
    centerlines = match_and_get_centerlines(road_segments)
    print(f"配对后得到游览中线数量：{len(centerlines)}")
    
    # 3. 计算路径特征指标
    metrics, turns, crosses = calculate_path_metrics(centerlines, GARDEN_AREA)
    
    # 4. 打印结果到控制台
    print("\n----- 路径特征指标 -----")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # 5. 保存结果到output文件夹
    output_file = os.path.join(OUTPUT_DIR, f'{GARDEN_NAME}_路径特征指标.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"园林名称：{GARDEN_NAME}\n")
        f.write("="*35 + "\n")
        f.write("路径提取方法：平行线段配对法提取游览中线\n")
        f.write("配对规则：平行夹角<15°、路宽0.5-3m、长度比<1.5\n")
        f.write("转折点阈值：偏转角度>30°\n")
        f.write("="*35 + "\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print(f"\n结果已保存到：{output_file}")
    print("问题1-1 完成！")