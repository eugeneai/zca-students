from interfaces import *
from zope.interface import implementer



@implementer(IStudent)
class Student(object):
    """Implements IStudent interface
    """

    def __init__(self, name, doc, group):
        """Initializes a student data.
        name is a given name and familyname of the student.
        doc is the number of student's document.
        """

        self.name=name
        self.doc=doc
        self.group=None
        self.move(group)

    def move(self, group):
        """Transfer the student to new group.

        Arguments:
        - `group`: a Group reference
        """

        if self.group!=None:
            self.group.remove_student(self)
            self.group=None
        # self.group == None
        group.add_student(self)

    def belongs_to(self, group):
        """Cheks that the student belogs to a group.
        """

        return self.group==group


@implementer(IGroup)
class Group(object):
    """Implements a group of students
    """

    def __init__(self, name):
        """Initializes group data
        """
        self.students=[]

    def add_student(self, student):
        """Adds a student to the group

        Arguments:
        - `student`: The student to be added.
        """
        if student.group==None:
            self.students.append(student)
            student.group=self
        else:
            raise ValueError("cannot add a student belonging to another group")

    def remove_student(self, student):
        """Remove a student from the group
        """
        if student.group==self:
            self.students.remove(student)
            student.group=None
        else:
            raise ValueError("student does not belong to the group")

    def size(self):
        """Returns size of the group
        """
        return len(self.students)


# provides = обслуживать, оснащать (экземпляры)
# implements = реализует (классы)


def test1():
    assert IGroup.implementedBy(Group), "This class does not provide IGroup"
    assert IStudent.implementedBy(Student), "This class does not provide IGroup"

    g1=Group("System Engineers")
    assert IGroup.providedBy(g1)
    g2=Group("Knowledge Engineer")
    assert IGroup.providedBy(g2)
    s1=Student("John Doe", 123456, g1)
    assert IStudent.providedBy(s1)
    s2=Student("Cameron Diaz", 123457, g2)
    assert IStudent.providedBy(s2)
    s3=Student("Jim Kerry", 123458, g1)
    assert IStudent.providedBy(s3)

    assert s3.belongs_to(g1)
    s3.move(g2)
    assert s3.belongs_to(g2)

    assert g2.size()==2
    assert g1.size()==1

    s3.send_down()
    assert s3.group==None
    assert g1.size()==0


if __name__=="__main__":
    test1()
    print("Ok")
    quit()
