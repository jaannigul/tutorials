from odoo import fields, models

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