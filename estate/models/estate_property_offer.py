from odoo import fields, models, api, exceptions
from datetime import date as dt_date
from dateutil.relativedelta import relativedelta
class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _sql_constraints=[
        ('check_offer_price','CHECK(price > 0)', 'Expected price must be greater than 0'),
    ]
    _order="price desc"

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status',
                              selection = [('accepted', 'Accepted'), ('refused', 'Refused')],
                              copy=False)
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True,string="Property")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            creation_date = offer.create_date.date() if offer.create_date else dt_date.today()
            offer.date_deadline = creation_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            creation_date = offer.create_date.date() if offer.create_date else dt_date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - creation_date).days

    def action_accept_offer(self):
        accepted_offer = self.search([
        ('property_id', '=', self.property_id.id),
        ('status', '=', 'accepted'),
        ('id', '!=', self.id)
    ])

        if accepted_offer:
            raise exceptions.UserError("An offer has already been accepted for this property.")

        self.status = 'accepted'

        
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.state = 'offer_accepted'

        return True

    def action_refuse_offer(self):
        self.status='refused'

        # clean buyer field if no accepted offers
        accepted_offer = self.search([('property_id', '=', self.property_id.id),('status', '!=','refused')])
        if not accepted_offer:
            self.property_id.buyer_id=False
            self.property_id.selling_price=0.0
            
        return True
        
