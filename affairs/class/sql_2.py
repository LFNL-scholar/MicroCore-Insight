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
txt_file_path = "订单表.txt"

# 先从 Customer 表中获取城市和 CustomerID 的映射
city_to_customer_id = {}
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT CustomerID, City FROM Customer")
    for row in cursor.fetchall():
        city_to_customer_id[row[1]] = row[0]
finally:
    cursor.close()
    connection.close()

# 读取 orders.txt 文件并解析数据
orders_data = []
order_id = 1  # 手动生成 OrderID，从 1 开始

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
            order_date = fields[1]  # 订单日期
            total_amount = float(fields[2])  # 订单总金额
            status = fields[3]  # 订单状态
            shipping_address = fields[4]  # 收货地址
            notes = fields[5] if fields[5] else None  # 备注

            # 根据收货地址的城市匹配 CustomerID
            city = shipping_address.split("市")[0] + "市" if "市" in shipping_address else None
            customer_id = city_to_customer_id.get(city)
            if not customer_id:
                print(f"未找到匹配的城市 {city}，跳过订单: {line}")
                continue

            orders_data.append((
                order_id,  # 手动添加 OrderID
                customer_id,
                order_date,
                total_amount,
                status,
                shipping_address,
                notes
            ))
            order_id += 1  # 递增 OrderID
except FileNotFoundError:
    print(f"文件 {txt_file_path} 未找到")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 插入 SQL 语句（包含 OrderID）
insert_query = """
INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount, Status, ShippingAddress, Notes)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# 批量插入数据
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    cursor.executemany(insert_query, orders_data)
    connection.commit()
    print(f"成功插入 {cursor.rowcount} 条记录到 Orders 表")

except pymysql.MySQLError as e:
    print(f"插入数据失败: {e}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()