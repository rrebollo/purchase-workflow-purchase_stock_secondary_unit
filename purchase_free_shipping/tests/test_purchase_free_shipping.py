# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import openerp.tests.common as common


class TestPurchaseOrder(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrder, self).setUp()
        self.model_purchase_order = self.env['purchase.order']
        self.model_res_partner = self.env['res.partner']
        self.model_stock_location = self.env['stock.location']
        self.model_product_pricelist = self.env['product.pricelist']

    def test_purchase_order_free_shipping(self):
        domain = [('supplier', '=', True)]
        partner_id = self.model_res_partner.search(domain, limit=1)
        location_id = self.model_stock_location.search([], limit=1)
        pricelist_id = self.model_product_pricelist.search([], limit=1)
        vals = {
            'partner_id': partner_id.id,
            'location_id': location_id.id,
            'pricelist_id': pricelist_id.id,
        }
        purchase_order_id = self.model_purchase_order.create(vals)
        self.assertEquals(
            purchase_order_id.free_shipping_amount,
            partner_id.free_shipping_amount, 'Should be the same')
        partner_id.free_shipping_amount = 1000
        self.assertEquals(
            purchase_order_id.free_shipping_amount,
            partner_id.free_shipping_amount, 'Should be the same')
