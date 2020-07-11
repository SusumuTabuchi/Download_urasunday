from logging import getLogger, StreamHandler, Formatter
import MySQLdb

logger = getLogger("__main__").getChild(__name__)

class MySQL:
    """
    MySQLを操作する
    """

    def __init__(self, DBsettings: dict):
        """
        Attributes
        ----------
        DBsettings : dict
            接続するDBのセッティング情報
        """
        self.connection = MySQLdb.connect(**DBsettings)
        self.cursor = self.connection.cursor()

    def query_execute(self, query_string: str):
        """
        SQL文を実行する
        Attributes
        ----------
        query_string : str
            実行するクエリ
        
        Returns
        -------
        result : tuple
            クエリ結果
        """
        try:
            self.cursor.execute(query_string)
        except Exception as e:
            self.connection_close()
            logger.error(e)
            logger.info("クエリを実行できませんでした。接続を終了します")
        return self.cursor.fetchall()
            

    def connection_close(self):
        self.connection.close()





if __name__ == "__main__":
    DBsettings = {
        "user": "urasunday_user",
        "passwd": "XXI2cvPIwHDnjw8w",
        "host": "localhost",
        "db": "urasunday",
        "charset": "utf8"
        }
    mysql = MySQL(DBsettings)
    sql = "SELECT * FROM `manga_master`"
    result = mysql.query_execute(sql)
    print(type(result))
    for row in result:
        print(row[1])
    mysql.connection.close()
