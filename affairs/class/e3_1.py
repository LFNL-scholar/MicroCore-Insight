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

        # --------------------- 增加：插入客户 ---------------------
        insert_customer = """
        INSERT INTO Customer (CustomerID, Name, ContactName, Phone, Email, Address, City, State, PostalCode, Country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_customer, (
            1002,  # CustomerID 是整数
            '未来科技有限公司', '张工', '13812345678',
            'zhanggong@example.com', '深圳市南山区科技园', '深圳', '广东', '518000', '中国'
        ))
        conn.commit()
        print("✅ 插入客户成功")

        # --------------------- 插入后查询：确认插入成功 ---------------------
        select_customer = "SELECT * FROM Customer WHERE CustomerID = %s"
        cursor.execute(select_customer, (1002,))
        result = cursor.fetchone()  # 查询插入的客户
        if result:
            print("✅ 查询客户成功，插入的数据如下：")
            print(result)
        else:
            print("❌ 插入的客户数据未能查询到")

        # --------------------- 删除：删除客户 ---------------------
        # delete_customer = "DELETE FROM Customer WHERE CustomerID = %s"
        # cursor.execute(delete_customer, (1002,))  # 删除 CustomerID 为 1002 的客户
        # conn.commit()
        # print("✅ 删除客户成功")

        # --------------------- 修改：更新客户信息 ---------------------
        update_customer = "UPDATE Customer SET City = %s, Address = %s WHERE CustomerID = %s"
        cursor.execute(update_customer, ('广州', '广州市天汇大厦', 1002))  # 假设修改 CustomerID 为 1002 的客户信息
        conn.commit()
        print("✅ 修改客户信息成功")

        # --------------------- 查询：查询指定客户 ---------------------
        select_customer = "SELECT * FROM Customer WHERE CustomerID = %s"
        cursor.execute(select_customer, (1002,))
        result = cursor.fetchone()  # 只查询一个客户
        if result:
            print("✅ 查询客户成功，结果如下：")
            print(result)
        else:
            print("❌ 未找到指定客户")

    except Exception as e:
        print("❌ 操作出错：", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
