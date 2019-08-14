from xiemizhe import XieMiZhe
from lu714 import Lu714
from thread_pool import FixThreadPool
from http_utils import HttpHelper
import schedule
import time
import cx_Oracle
import os


# Create the session pool
pool = cx_Oracle.SessionPool("sdk_user", "sdk_user",
                             "172.18.0.68:1521/sdk:SDK_USER", min=2, max=50, increment=1, encoding="UTF-8")
thread_pool = FixThreadPool()


def check_db_item_exists(dt):
    connection = pool.acquire()
    cursor = connection.cursor()
    result = cursor.execute("SELECT count(1) FROM GRAB_THIRD_WEBSITE_EXTEND t "
                            "where t.APP_NAME = :app_name and t.APP_TYPE = :type_name", dt)
    data = result.fetchall()
    pool.release(connection)
    count = data[0]
    if count[0] > 0:
        return True
    else:
        return False


def batch_insert_data(bulk):
    for sub_data in bulk.data:
        for app in sub_data.appInfo:
            connection = pool.acquire()
            cursor = connection.cursor()
            dt = {
                "app_name": app["app_name"],
                "type_name": sub_data.name
            }
            if not check_db_item_exists(dt):
                dt["url"] = app["link"]
                print(bulk.name, "insert new record: ", dt["app_name"], dt["type_name"])
                cursor.execute("INSERT INTO GRAB_THIRD_WEBSITE_EXTEND(ID, APP_NAME, APP_TYPE, URL) "
                               "VALUES (GRAB_THIRD_WEBSITE_SEQ.nextval, :app_name, :type_name, :url)", dt)
                connection.commit()
            else:
                print(bulk.name, "insert exit record: ", dt["app_name"], dt["type_name"], " this will skip .")
            pool.release(connection)


def job():
    start = time.time()
    print("job working, start at: ",start)
    try:
        r1 = XieMiZhe()
        r1.start(thread_pool)
        thread_pool.job_queue.join()
        print(r1.data)
        batch_insert_data(r1)

        r2 = Lu714()
        r2.start(thread_pool)
        thread_pool.job_queue.join()
        print(r2.data)
        batch_insert_data(r2)

    except Exception as e:
        print('Error:', e)
    finally:
        end = time.time()
        print('job end at: ', end, 'spent: ', (end - start), 'ms')


job()

# schedule.every(10).seconds.do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

thread_pool.shutdown()
pool.close()





