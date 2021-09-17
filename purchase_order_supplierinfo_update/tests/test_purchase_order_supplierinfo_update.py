# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase


class TestPurchaseOrderSupplierinfoUpdate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product Test", "type": "product"}
        )
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier Test"})
        cls.supplierinfo = cls.env["product.supplierinfo"].create(
            {
                "name": cls.supplier.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "price": 100,
            }
        )

    def test_confirn_purchase_order(self):
        # Create a PO, confirm it and check the supplierinfo is updated
        po_form = Form(self.env["purchase.order"])
        po_form.partner_id = self.supplier
        with po_form.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            self.assertEqual(po_line_form.price_unit, 100)
            po_line_form.price_unit = 150
            po_line_form.taxes_id.clear()
        purchase_order = po_form.save()
        purchase_order.button_confirm()
        self.assertEqual(self.supplierinfo.price, 150)
        # Create another PO, confirm it and check the supplierinfo is updated
        po_form = Form(self.env["purchase.order"])
        po_form.partner_id = self.supplier
        with po_form.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            self.assertEqual(po_line_form.price_unit, 150)
            po_line_form.price_unit = 200
            po_line_form.taxes_id.clear()
        purchase_order = po_form.save()
        purchase_order.button_confirm()
        self.assertEqual(self.supplierinfo.price, 200)

    def test_change_price_in_confirmed_po(self):
        # Create first purchase
        po_form_1 = Form(self.env["purchase.order"])
        po_form_1.partner_id = self.supplier
        with po_form_1.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            po_line_form.taxes_id.clear()
        purchase_order_1 = po_form_1.save()
        purchase_order_1.button_confirm()
        # Create second purchase
        po_form_2 = Form(self.env["purchase.order"])
        po_form_2.partner_id = self.supplier
        with po_form_2.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            po_line_form.price_unit = 200
            po_line_form.taxes_id.clear()
        purchase_order_2 = po_form_2.save()
        purchase_order_2.button_confirm()
        # Change price in second purchase
        with Form(purchase_order_2) as po_form_2:
            with po_form_2.order_line.edit(0) as po_line_form:
                po_line_form.price_unit = 300
        self.assertEqual(self.supplierinfo.price, 300)
        # Change price in first purchase. This doesn't update supplierinfo
        # because it isn't the last purchase of this product by this supplier
        with Form(purchase_order_1) as po_form_1:
            with po_form_1.order_line.edit(0) as po_line_form:
                po_line_form.price_unit = 400
        self.assertEqual(self.supplierinfo.price, 300)

    def test_create_new_line_in_a_confirmed_po(self):
        # Create first purchase
        po_form_1 = Form(self.env["purchase.order"])
        po_form_1.partner_id = self.supplier
        with po_form_1.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            po_line_form.taxes_id.clear()
        purchase_order_1 = po_form_1.save()
        purchase_order_1.button_confirm()
        # Create second purchase
        po_form_2 = Form(self.env["purchase.order"])
        po_form_2.partner_id = self.supplier
        with po_form_2.order_line.new() as po_line_form:
            po_line_form.product_id = self.product
            po_line_form.price_unit = 200
            po_line_form.taxes_id.clear()
        purchase_order_2 = po_form_2.save()
        purchase_order_2.button_confirm()
        # Create a new line in the first purchase (that is already confirmed)
        # with another product.
        product_2 = self.env["product.product"].create(
            {"name": "Product Test 2", "type": "product"}
        )
        supplierinfo_2 = self.env["product.supplierinfo"].create(
            {
                "name": self.supplier.id,
                "product_tmpl_id": product_2.product_tmpl_id.id,
                "price": 10,
            }
        )
        with Form(purchase_order_1) as po_form:
            with po_form.order_line.new() as po_line_form:
                po_line_form.product_id = product_2
                po_line_form.price_unit = 20
        self.assertEqual(supplierinfo_2.price, 20)
