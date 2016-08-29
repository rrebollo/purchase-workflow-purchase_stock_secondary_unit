# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    free_shipping_amount = fields.Float(
        compute='_compute_free_shipping_amount',
        string='Free Shipping Minimum Amount',
        compute_sudo=False)

    @api.multi
    @api.depends('partner_id.free_shipping_amount')
    def _compute_free_shipping_amount(self):
        for rec in self:
            rec.free_shipping_amount = rec.partner_id.free_shipping_amount
