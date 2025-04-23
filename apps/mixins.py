from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    """Reusable mixin for timestamps to keeps things DRY"""
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class BaseMixin(models.Model):
    """resusable and extensible mixin"""
    is_published = models.BooleanField(_("Active?"), default=True)

    class Meta:
        abstract = True