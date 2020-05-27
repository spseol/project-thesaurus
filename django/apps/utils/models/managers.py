from django.db.models import Manager


class BaseTypeModelManager(Manager):
    def get_by_identifier(self, identifier):
        return super().get_or_create(identifier=identifier)[0]
