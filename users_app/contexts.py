from .permissions import (
    has_admin_permission,
    has_moderator_permission,
    has_teacher_permission,
    has_employee_permission,
    has_student_permission,
)

def user_permissions(request):
    return {
        'user_permissions': {
            'admin': has_admin_permission(request.user),
            'moderator': has_moderator_permission(request.user),
            'teacher': has_teacher_permission(request.user),
            'employee': has_employee_permission(request.user),
            'student': has_student_permission(request.user),
        }
    }