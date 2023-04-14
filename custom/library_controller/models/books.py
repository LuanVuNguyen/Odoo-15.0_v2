from odoo import models, fields, api
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    x_RFID = fields.Char(string='RFID')