from odoo import fields, models, api, exceptions
from datetime import date
from dateutil.relativedelta import relativedelta
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _sql_constraints=[
        ('check_expected_price','CHECK expected_price > 0',),
        ('check_selling_price','CHECK selling_price > 0'),
        ('check_property_type_name'),
    ]

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
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (m²)")
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
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Price"
    )
    best_price = fields.Float(compute="_compute_best_price")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif self.garden is False:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold_button(self):
        for prop in self:
            if prop.state != 'cancelled':
              prop.state = 'sold'
              return True
            elif prop.state == 'cancelled':
                raise exceptions.UserError('Cancelled properties can not be sold.')

    def action_cancelled_button(self):
        for prop in self:
            if prop.state != 'sold':
              prop.state = 'cancelled'
              return True
            elif prop.state == 'sold':
                raise exceptions.UserError('Sold properties can not be cancelled.')