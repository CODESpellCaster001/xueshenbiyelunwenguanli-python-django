from rolepermissions.roles import get_user_roles


def get_name_role(request):
    user = request.user
    name = user.name
    try:
        role = get_user_roles(user)[0].get_cls_name()
    except IndexError:
        role = '无角色'

    return name, role
