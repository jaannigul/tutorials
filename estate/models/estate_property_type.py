from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints=[
        ('check_property_type_name','UNIQUE (name)',),
    ]
    name = fields.Char(string='Property Type', required=True)