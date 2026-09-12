#common/config.py
#全局常量配置，所有阶段公用

# 单位转换：原始数据是毫米(mm)，我们统一转成米(m)
MM_TO_M=0.001


# 数据清洗的阈值
MIN_SEGMENT_LENGTH=1.0  # 长度小于1米的碎线段，直接丢掉

MAX_PLANT_RADIUS=20.0  # # 植物冠径超过20米，算异常数据

SIGMA_TIMES=3  # 统计学中，超过均值3倍标准差的点，算异常数据