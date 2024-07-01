from rolepermissions.roles import AbstractUserRole


class Teacher(AbstractUserRole):
    available_permissions = {
    }

    @staticmethod
    def get_cls_name():
        return "教师"


class Student(AbstractUserRole):
    available_permissions = {
    }

    @staticmethod
    def get_cls_name():
        return "学生"


class Admin(AbstractUserRole):
    available_permissions = {
    }

    @staticmethod
    def get_cls_name():
        return "管理员"



