from django.db.models import Manager


class BaseTypeModelManager(Manager):
    def get_by_identifier(self, identifier):
        return super().get(identifier=identifier)
