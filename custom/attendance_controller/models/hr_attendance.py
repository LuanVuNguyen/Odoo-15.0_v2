from odoo import fields, models, api


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    checkin_image = fields.Char()
    checkout_image = fields.Char()
