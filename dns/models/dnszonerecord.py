# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## DNSZoneRecord model
##----------------------------------------------------------------------
## Copyright (C) 2007-2012 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------

## Django modules
from django.utils.translation import ugettext_lazy as _
from django.db import models
## NOC modules
from dnszone import DNSZone
from dnszonerecordtype import DNSZoneRecordType
from noc.lib.fields import AutoCompleteTagsField
from noc.lib.app.site import site


class DNSZoneRecord(models.Model):
    """
    Zone RRs
    """
    class Meta:
        verbose_name = _("DNS Zone Record")
        verbose_name_plural = _("DNS Zone Records")
        db_table = "dns_dnszonerecord"
        app_label = "dns"

    zone = models.ForeignKey(DNSZone, verbose_name="Zone")
    left = models.CharField(_("Left"), max_length=32, blank=True, null=True)
    type = models.ForeignKey(DNSZoneRecordType, verbose_name="Type")
    # @todo: Priority
    # @todo: TTL
    right = models.CharField(_("Right"), max_length=64)
    tags = AutoCompleteTagsField(_("Tags"), null=True, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self.zone.name,
            " ".join([x
                      for x
                      in (self.left, self.type.type, self.right)
                      if x is not None
                    ]))

    def get_absolute_url(self):
        """Return link to zone preview

        :return: URL
        :rtype: String
        """
        return site.reverse("dns:dnszone:change", self.zone.id)

    def save(self, *args, **kwargs):
        super(DNSZoneRecord, self).save(*args, **kwargs)
        # Refresh zone cache
        self.zone.touch(self.zone.name)

    def delete(self, *args, **kwargs):
        zone = self.zone
        super(DNSZoneRecord, self).delete(*args, **kwargs)
        zone.touch(zone.name)
