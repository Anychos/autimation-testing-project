from enum import StrEnum


class Epic(StrEnum):
    API = "API"
    UI = "UI"


class Feature(StrEnum):
    AUTHORIZATION = "Authorization"
    TASKS = "Tasks"


class Story(StrEnum):
    LOGIN = "Login"
    REGISTRATION = "Registration"
    TASKS_GET = "Tasks_Get"
    TASKS_CREATE = "Tasks_Create"
    TASKS_EDIT = "Tasks_Edit"
    TASKS_DELETE = "Tasks_Delete"


class Severity(StrEnum):
    CRITICAL = "Critical"
    MAJOR = "Major"
    MEDIUM = "Medium"
