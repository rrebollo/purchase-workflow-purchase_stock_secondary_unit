# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):
        """
        If there is a purchase order and a fiscal position on it which have exactly
        one purchase journal allowed, set this journal on the invoice.
        """
        # We need to save de PO because the origin method unset it
        purchase_order = self.purchase_id
        res = super()._onchange_purchase_auto_complete()
        fiscal_position = purchase_order.fiscal_position_id
        if fiscal_position:
            purchase_journals = fiscal_position.allowed_journal_ids.filtered(
                lambda j: j.type == "purchase"
            )
            if len(purchase_journals) == 1:
                self.journal_id = purchase_journals
        return res
