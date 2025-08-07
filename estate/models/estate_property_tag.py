from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints=[
        ('check_property_tag_name','UNIQUE(name)','Property tag name must be unique'),
    ]
    _order="name"

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer(string="Color", default=1)