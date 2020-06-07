def has_admin_permission(user, eesuser=None):
    if not user.is_authenticated:
        return False
    if not eesuser:
        eesuser = user.eesuser
    if getattr(user, 'is_superuser') or getattr(eesuser, 'is_admin'):
        return True
    return False

def has_moderator_permission(user, eesuser=None):
    if not user.is_authenticated:
        return False
    if not eesuser:
        eesuser = user.eesuser
    if getattr(eesuser, 'is_moderator') or has_admin_permission(user, eesuser):
        return True
    return False

def has_teacher_permission(user, eesuser=None):
    if not user.is_authenticated:
        return False
    if not eesuser:
        eesuser = user.eesuser
    if getattr(eesuser, 'is_teacher') or has_admin_permission(user, eesuser):
        return True
    return False

def has_employee_permission(user, eesuser=None):
    if not user.is_authenticated:
        return False
    if not eesuser:
        eesuser = user.eesuser
    if getattr(eesuser, 'is_employee') or has_teacher_permission(user, eesuser):
        return True
    return False

def has_student_permission(user, eesuser=None):
    if not user.is_authenticated:
        return False
    if not eesuser:
        eesuser = user.eesuser
    if getattr(eesuser, 'is_student') or has_employee_permission(user, eesuser):
        return True
    return False