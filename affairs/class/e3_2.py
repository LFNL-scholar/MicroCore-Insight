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

def main():
    try:
        # 连接数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # --------------------- 查找当前最大 OrderID ---------------------
        cursor.execute("SELECT MAX(OrderID) FROM Orders")
        result = cursor.fetchone()
        # 如果表为空，则从1开始
        new_order_id = result[0] + 1 if result[0] is not None else 1

        # --------------------- 插入订单 ---------------------
        insert_order = """
        INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount, Status, ShippingAddress, Notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        order_data = (new_order_id, 1, '2025-03-20 00:00:00', 1500000.00, '已支付', '江苏省镇江市江苏科技大学计算机学院', '顺丰快递')
        cursor.execute(insert_order, order_data)
        conn.commit()
        print("✅ 插入订单成功，OrderID:", new_order_id)

    except Exception as e:
        print("❌ 操作出错：", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
