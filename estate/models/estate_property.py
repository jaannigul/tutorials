from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="Property Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True,string="Expected Price",default=None)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (m²)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (m²)")
    garden_orientation = fields.Selection(
        selection=[('south', 'South'), ('north', 'North'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
    )
    active = fields.Boolean(default=True, string="Active")
    state=fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                    ('offer_accepted', 'Offer Accepted'),
                      ('sold', 'Sold'), ('cancelled', 'Cancelled')],
                        default='new',
                        string="State",)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)