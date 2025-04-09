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

        # --------------------- 查找当前最大 ScheduleID ---------------------
        cursor.execute("SELECT MAX(ScheduleID) FROM ProductionSchedule")
        result = cursor.fetchone()
        # 如果表为空，则从1开始
        new_schedule_id = result[0] + 1 if result[0] is not None else 1

        # --------------------- 插入排产记录 ---------------------
        insert_schedule = """
        INSERT INTO ProductionSchedule (ScheduleID, OrderID, Quantity, StartDate, EndDate, Status, Notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        schedule_data = (new_schedule_id, 1, 100, '2025-03-21 00:00:00', '2025-03-25 00:00:00', '进行中', '生产排产')
        cursor.execute(insert_schedule, schedule_data)
        conn.commit()
        print("✅ 插入排产记录成功，ScheduleID:", new_schedule_id)

    except Exception as e:
        print("❌ 操作出错：", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
