from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints=[
        ('check_property_type_name','UNIQUE(name)','Property type name must be unique'),
    ]
    _order="sequence,name"

    name = fields.Char(string='Property Type', required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")


    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_ids.mapped('offer_ids'))