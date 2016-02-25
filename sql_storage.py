import sqlite3 as sql
from interfaces import *
from zope.component import adapter, getGlobalSiteManager
from zope.interface import implementer
from components import test_students

@implementer(ISQLiteStorage)
class SQLiteStorage(object):
    """Stores objects into SQLite database.
    """

    def __init__(self, filename):
        """
        """

        self.filename=filename
        self.conn=sql.connect(self.filename)
        self.create_tables()

    def store(self, obj):
        o=ISQLiteStorable(obj)
        return o.store_in(self)

    def get(self, obj_id):
        pass

    def create_tables(self):
        cur=self.conn.cursor()

        cur.executescript("""

            DROP TABLE IF EXISTS Students;
            DROP TABLE IF EXISTS Groups;

            CREATE TABLE IF NOT EXISTS Students (
               name text,
               doc text,
               group_id integer
            );

            CREATE TABLE IF NOT EXISTS Groups (
               name text
            );

            """)
        self.conn.commit()

@implementer(ISQLiteStorable)
@adapter(IStudent)
class IStudentToISQLiteStorableAdapter(object):
    table="Students"
    def __init__(self, student):
        self.student=student

    def store_in(self, storage):
        conn=storage.conn
        student=self.student
        assert hasattr(student.group, "sql_id")

        cur=conn.cursor()
        cur.execute("""INSERT INTO Students
                    (name, doc, group_id)
                    VALUES
                    (?, ?, ?)""",
                    (student.name, student.doc,
                     student.group.sql_id)
        )
        rc=cur.lastrowid
        conn.commit()
        return rc

@implementer(ISQLiteStorable)
@adapter(IGroup)
class IGroupToISQLStorableAdapter(object):
    table="Groups"
    def __init__(self, group):
        self.group=group

    def store_in(self, storage):
        conn=storage.conn
        cur=conn.cursor()
        cur.execute("""INSERT INTO Groups (name)
                    VALUES
                    (?)""", (self.group.name, )
        )
        rc=cur.lastrowid
        self.group.sql_id=rc
        conn.commit()
        for s in self.group.students:
            storage.store(s)
        return rc

GSM=getGlobalSiteManager()
GSM.registerAdapter(IGroupToISQLStorableAdapter)
GSM.registerAdapter(IStudentToISQLiteStorableAdapter)

def test_sore():
    storage=SQLiteStorage("university_test.db")
    test_students(storage)


if __name__=="__main__":
    test_sore()
    print ("Ok")
    quit()
