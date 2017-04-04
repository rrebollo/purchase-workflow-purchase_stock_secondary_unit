# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.constrains('purchase_request', 'purchase_requisition')
    def _check_request_requisition(self):
        for product in self:
            if product.purchase_request and \
                    product.purchase_requisition == 'tenders':
                raise ValidationError(_('Only one selection of Purchase '
                                        'Request or Call for Bids allowed'))
        return True
