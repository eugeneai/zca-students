import sqlite3 as sql
from interfaces import *
#from zope.component import adapter, getGlobalSiteManager
from zope.interface import implementer
from components import test_students, Group, Student
from zope.component import getUtility, getAdapter

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

    def get(self, obj_id, class_):
        obj=class_(stub=True)
        o=ISQLiteStorable(obj)
        try:
            o.get_from(self, obj_id)
        except KeyError:
            return None
        return obj

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

#@implementer(ISQLiteStorable)
#@adapter(IStudent)
class AdapterOfIStudentToISQLiteStorable(object):
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

    def get_from(self, storage, obj_id):
        conn=storage.conn
        cur=conn.cursor()
        cur.execute("""
                    SELECT * FROM Students
                    WHERE
                    rowid=?""", (obj_id,))
        data=cur.fetchone()
        name, doc, _=data
        s=Student(name=name, doc=int(doc))
        s.sql_id=obj_id

#@implementer(ISQLiteStorable)
#@adapter(IGroup)
class AdapterOfIGroupToISQLiteStorable(object):
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

    def get_from(self, storage, obj_id):
        conn=storage.conn
        cur=conn.cursor()
        cur.execute("""SELECT * FROM Groups
                    WHERE
                    rowid=?""", (obj_id,))
        rc=cur.fetchone()
        if rc:
            self.group.name=rc[0]
            cur.execute("""SELECT rowid,* FROM Students
                        WHERE
                        group_id=?
                        """, (obj_id,))
            rows=cur.fetchall()
            for srowid, name, doc, _ in rows:
                s=Student(name=name, doc=int(doc),
                    group=self.group)
                s.sql_id=srowid
            self.group.sql_id=obj_id


storage=SQLiteStorage("university_test.db")


def test_sore():
    s=getUtility(ISQLiteStorage)
    test_students(s)


if __name__=="__main__":
    from zope.configuration.xmlconfig import xmlconfig
    xmlconfig(open("config.zcml","r"))
    print("""


          """)
    test_sore()
    print ("Ok")
    quit()
