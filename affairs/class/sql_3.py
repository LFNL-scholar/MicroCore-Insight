import pymysql

# 数据库连接配置
db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "LFNL",
    "database": "bigdata",
    "charset": "utf8mb4"
}

# TXT 文件路径
txt_file_path = "排产表数据.txt"

# 先从 Orders 表中获取有效的 OrderID
valid_order_ids = set()
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT OrderID FROM Orders")
    for row in cursor.fetchall():
        valid_order_ids.add(row[0])
    print("Orders 表中的有效 OrderID:", valid_order_ids)
finally:
    cursor.close()
    connection.close()

# 读取 production_schedules.txt 文件并解析数据
production_schedules_data = []
schedule_id = 1  # 手动生成 ScheduleID，从 1 开始

try:
    with open(txt_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # 跳过表头
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            # 按制表符分隔
            fields = line.split("\t")
            if len(fields) != 6:
                print(f"跳过无效行: {line}")
                continue
            # 提取字段
            order_id = int(fields[0])  # 序列（对应 OrderID）
            quantity = int(fields[1])  # 生产数量
            start_date = fields[2]  # 生产开始日期
            end_date = fields[3]  # 生产结束日期
            status = fields[4]  # 排产状态
            notes = fields[5] if fields[5] else None  # 备注

            # 验证 OrderID 是否存在
            if order_id not in valid_order_ids:
                print(f"OrderID {order_id} 在 Orders 表中不存在，跳过排产记录: {line}")
                continue

            production_schedules_data.append((
                schedule_id,  # 手动添加 ScheduleID
                order_id,
                quantity,
                start_date,
                end_date,
                status,
                notes
            ))
            schedule_id += 1  # 递增 ScheduleID
except FileNotFoundError:
    print(f"文件 {txt_file_path} 未找到")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 插入 SQL 语句（包含 ScheduleID）
insert_query = """
INSERT INTO ProductionSchedule (ScheduleID, OrderID, Quantity, StartDate, EndDate, Status, Notes)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# 批量插入数据
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    cursor.executemany(insert_query, production_schedules_data)
    connection.commit()
    print(f"成功插入 {cursor.rowcount} 条记录到 ProductionSchedule 表")

except pymysql.MySQLError as e:
    print(f"插入数据失败: {e}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()