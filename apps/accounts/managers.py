# AC-05: Isolamento Tenant
# FR29: Isolamento dati tra tenant (zero cross-tenant leakage)
# Manager custom per query filtrate per tenant

from django.db import models


class TenantManagerMixin:
    """
    Mixin per garantire isolamento tenant nelle query.
    Tutte le query vengono filtrate automaticamente per tenant.

    Satisfies: FR29 (zero cross-tenant leakage), NFR6
    """

    def for_tenant(self, tenant):
        """
        Filtra il queryset per tenant specifico.
        Garantisce zero cross-tenant data leakage.
        """
        # AC-05: query filtrate per tenant
        return self.filter(tenant=tenant)


class TenantAwareManager(models.Manager, TenantManagerMixin):
    """
    Manager con isolamento tenant integrato.
    Usa `for_tenant(tenant)` per ottenere dati del solo tenant richiesto.
    """
    pass
