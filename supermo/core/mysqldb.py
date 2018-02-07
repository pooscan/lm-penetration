import config.config as conf
import pymysql as mdb
import time
class mysqldb(object):
    def create_db(self):
        # 创建数据库
        drop_db_str = 'drop database if exists ' + conf.DB['DB_NAME'] + ' ;'
        create_db_str = 'create database ' +conf.DB['DB_NAME'] + ' ;'
        conn = mdb.connect(conf.DB['HOST'], conf.DB['USER'], conf.DB['PASSWORD'])
        cursor = conn.cursor()
        try:
            cursor.execute(drop_db_str)
            cursor.execute(create_db_str)
            conn.commit()
        except OSError:
            print("无法创建数据库！")
        finally:
            cursor.close()
            conn.close()
    def create_valid_ip(self):
        """
        创建数据库用于保存有效ip
        """
        # 选择该数据库
        use_db_str = 'use ' + conf.DB['DB_NAME'] + ' ;'
        # 创建表格
        create_table_valid_ip = """CREATE TABLE valid_ip (
          `content` varchar(30) NOT NULL,
          `test_times` int(5) NOT NULL DEFAULT '0',
          `failure_times` int(5) NOT NULL DEFAULT '0',
          `success_rate` float(5,2) NOT NULL DEFAULT '0.00',
          `avg_response_time` float NOT NULL DEFAULT '0',
          `score` float(5,2) NOT NULL DEFAULT '0.00'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        # 连接数据库
        conn = mdb.connect(conf.DB['HOST'],conf.DB['USER'],conf.DB['PASSWORD'])
        cursor = conn.cursor()
        try:
            cursor.execute(use_db_str)
            cursor.execute("DROP TABLE IF EXISTS valid_ip")
            cursor.execute(create_table_valid_ip)
            conn.commit()
        except OSError:
            print("无法创建数据库！")
        finally:
            cursor.close()
            conn.close()
    def create_table_crawlurl(self):
        # 选择该数据库
        use_db_str = 'use ' + conf.DB['DB_NAME'] + ' ;'
        # 创建表格
        create_table_crawlurl = """CREATE TABLE crawlurl (
          `id` int(11) UNSIGNED NOT NULL,
          `taskname` VARCHAR(100) NOT NULL,
          `url` VARCHAR(200) NOT NULL,
          `results` VARCHAR(2) NOT NULL DEFAULT '0',
          `scantime` VARCHAR(100) NOT NULL ,          
          `status` TINYINT(1) NOT NULL DEFAULT '1'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        # 连接数据库
        conn = mdb.connect(conf.DB['HOST'],conf.DB['USER'],conf.DB['PASSWORD'])
        cursor = conn.cursor()
        try:
            cursor.execute(use_db_str)
            cursor.execute("DROP TABLE IF EXISTS crawlurl")
            cursor.execute(create_table_crawlurl)
            conn.commit()
        except OSError:
            print("无法创建数据库！")
        finally:
            cursor.close()
            conn.close()
    def create_table_website(self):
        use_db_str = 'use ' + conf.DB['DB_NAME'] + ' ;'
        # 创建表格
        create_table_website = """CREATE TABLE website (
          `id` int(11) UNSIGNED NOT NULL,
          `taskname` VARCHAR(100) NOT NULL,
          `website` VARCHAR(100) NOT NULL,
          `company` VARCHAR(140) NOT NULL DEFAULT '0',          
          `addtime` VARCHAR(220 ) NOT NULL,          
          `status` TINYINT(1) NOT NULL DEFAULT '1'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        # 连接数据库
        conn = mdb.connect(conf.DB['HOST'],conf.DB['USER'],conf.DB['PASSWORD'])
        cursor = conn.cursor()
        try:
            cursor.execute(use_db_str)
            cursor.execute("DROP TABLE IF EXISTS website")
            cursor.execute(create_table_website)
            conn.commit()
        except OSError:
            print("无法创建数据库！")
        finally:
            cursor.close()
            conn.close()

    # 写入数据库

    def insertCrawl(project_name,page_url):
        db = mdb.connect(conf.DB['HOST'], conf.DB['USER'], conf.DB['PASSWORD'], conf.DB['DB_NAME'])
        cursor = db.cursor()
        sql = "INSERT INTO crawlurl(taskname,url,scantime) VALUES('%s','%s','%s')" %(project_name,page_url,time.time())
        try:
            # 执行SQL语句
            cursor.execute(sql)
            db.commit()
        except OSError as e:
            db.rollback()
        db.close()