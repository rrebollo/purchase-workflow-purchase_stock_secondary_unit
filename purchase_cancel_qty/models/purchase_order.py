# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def button_approve(self):
        res = super(PurchaseOrder, self).button_approve()
        for rec in self:
            rec._update_lines_ordered_qty()
        return res

    @api.multi
    def _update_lines_ordered_qty(self):
        self.ensure_one()
        for line in self.order_line:
            line.write({
                'ordered_qty': line.product_qty,
            })
