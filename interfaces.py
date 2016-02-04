from zope.interface import Interface, Attribute

class IStudent(Interface):
    """This interface defines schema for student
    component.
    """

    name=Attribute("Name of the student")
    doc=Attribute("Number of document")
    group=Attribute("A group of the student")

    def move(group):
        """Add the student to a group."""

    def send_down():
        """Send down the student from the university."""

    def belongs_to(group):
        """Checks wether the student belongs to a group"""

class IGroup(Interface):
    """Defines shcema and methods for student group
    """

    name=Attribute("Name of the group")
    students=Attribute("List of the students belonging to the group")

    def add_student(student):
        """Adds a student to the group"""

    def remove_student(student):
        """Removes a student from the group"""

    def disperse():
        """Remove all the student from the group"""
