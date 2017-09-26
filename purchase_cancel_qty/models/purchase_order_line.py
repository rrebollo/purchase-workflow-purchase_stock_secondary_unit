# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError

PRODUCT_QTY_READONLY_STATES = {
    'purchase': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

CANCELLED_QTY_EDITABLE_STATES = {
    'purchase': [('readonly', False)],
}


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    product_qty = fields.Float(
        states=PRODUCT_QTY_READONLY_STATES
    )
    ordered_qty = fields.Float(
        string="Ordered Qty",
        readonly=True,
        copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
    )
    cancelled_qty = fields.Float(
        string="Cancelled Qty",
        readonly=True,
        copy=False,
        inverse='_inverse_cancelled_qty',
        track_visibility='onchange',
        digits=dp.get_precision('Product Unit of Measure'),
        states=CANCELLED_QTY_EDITABLE_STATES,
    )

    @api.multi
    def _inverse_cancelled_qty(self):
        for rec in self:
            rec.product_qty = rec.ordered_qty - rec.cancelled_qty

    @api.multi
    @api.constrains('cancelled_qty', 'ordered_qty')
    def _check_cancelled_qty(self):
        for rec in self:
            if rec.cancelled_qty < 0:
                raise ValidationError(
                    _("Cancelled quantity must be greater or equal to 0."))
            if rec.cancelled_qty > rec.ordered_qty:
                raise ValidationError(
                    _("Cancelled quantity can't be greater than "
                      "ordered quantity."))
