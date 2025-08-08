from odoo import models, fields

class EstateProperty(models.Model):
    _inherit="estate.property"

    def action_sold_button(self):
        print("inherited method")
        res = super().action_sold_button()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type"
                }
            )