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
txt_file_path = "客户表数据.txt"

# 读取 customers.txt 文件并解析数据
customers_data = []
current_customer = {}
customer_id = 1  # 手动生成 CustomerID，从 1 开始

try:
    with open(txt_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:  # 空行表示一条记录结束
                if current_customer:
                    customers_data.append((
                        customer_id,  # 手动添加 CustomerID
                        current_customer["客户名称"],
                        current_customer.get("联系人姓名"),
                        current_customer.get("联系电话"),
                        current_customer.get("电子邮件"),
                        current_customer.get("地址"),
                        current_customer.get("城市"),
                        current_customer.get("省份"),
                        current_customer.get("邮政编码"),
                        current_customer.get("国家")
                    ))
                    customer_id += 1  # 递增 CustomerID
                    current_customer = {}
                continue
            # 解析字段
            key, value = line.split("：", 1)
            current_customer[key] = value.strip()
        # 处理最后一条记录
        if current_customer:
            customers_data.append((
                customer_id,
                current_customer["客户名称"],
                current_customer.get("联系人姓名"),
                current_customer.get("联系电话"),
                current_customer.get("电子邮件"),
                current_customer.get("地址"),
                current_customer.get("城市"),
                current_customer.get("省份"),
                current_customer.get("邮政编码"),
                current_customer.get("国家")
            ))
except FileNotFoundError:
    print(f"文件 {txt_file_path} 未找到")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 插入 SQL 语句（包含 CustomerID）
insert_query = """
INSERT INTO Customer (CustomerID, Name, ContactName, Phone, Email, Address, City, State, PostalCode, Country)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# 批量插入数据
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    cursor.executemany(insert_query, customers_data)
    connection.commit()
    print(f"成功插入 {cursor.rowcount} 条记录到 Customer 表")

except pymysql.MySQLError as e:
    print(f"插入数据失败: {e}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()