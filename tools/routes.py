from enum import StrEnum


class Route(StrEnum):
    REGISTER = "/api/v1/auth/register"
    LOGIN = "/api/v1/auth/login"
    GET_USER_ME = "/api/v1/auth/me"
    GET_CSRF = "/api/v1/auth/csrf"
    LOGOUT = "/api/v1/auth/logout"

    TASKS = "/api/v1/tasks"

    HEALTH = "/health"
