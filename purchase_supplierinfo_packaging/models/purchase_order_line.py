# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_is_zero


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    def _compute_product_packaging_id(self):
        res = super()._compute_product_packaging_id()
        for rec in self:
            rec._suggest_seller_packaging()
        return res

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        uom = self.product_uom
        if uom and not float_is_zero(self.product_qty, precision_rounding=uom.rounding):
            self.product_packaging_qty = self.product_qty
        return super()._onchange_product_packaging_id()

    def _suggest_seller_packaging(self):
        self.ensure_one()
        product = self.product_id
        uom = self.product_uom
        if not product or not uom or self.product_packaging_id:
            return
        order = self.order_id
        order_date = order.date_order

        params = {"order_id": order}
        seller = product._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=order_date.date() if order_date else fields.Date.context_today(self),
            uom_id=uom,
            params=params,
        )
        if not seller:
            return
        self.product_packaging_id = seller.packaging_id
