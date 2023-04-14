from odoo import fields, models
class SchoolProfile(models.Model):
    _name = "attendance.video"
    _inherit = "hr.attendance"
    attendance_id = fields.Many2one('hr.attendance', string="attendance id")
    checkin_video=fields.Text(string="Check In Video link")
    checkout_video=fields.Text(string="Check Out Video link")


