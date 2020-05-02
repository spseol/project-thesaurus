from rest_framework.permissions import DjangoModelPermissions


class RestrictedViewModelPermissions(DjangoModelPermissions):
    """
    Same as parent, but requires also app.view_model perm for retrieve/list.
    """
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
    }
