from odoo import models, fields, api


class AttendanceCustom(models.Model):
    _inherit = "hr.attendance"
    video_base64 = fields.Text(string="Video Base64 Check In", compute="_compute_video_base64")
    video_base64_checkout = fields.Text(string="Video Base64 Check Out", compute="_compute_video_base64_checkout")
    tracking_video = fields.Html("Video Check In", sanitize=False, compute='get_html')
    tracking_video_checkout = fields.Html("Video Check Out", sanitize=False, compute='get_html_checkout')

    @api.depends('check_in')
    def get_html(self):
        for attendance in self:
            if attendance.video_base64 != False:
                attendance.tracking_video = f'<video width="320" height="240" controls=""><source src="data:video/mp4;base64,{ attendance.video_base64 }" type="video/mp4"/></video>'
            else:
                attendance.tracking_video =f'<field name="video_base64"/>'
    @api.depends('check_in')
    def _compute_video_base64(self):
        for attendance in self:
            if attendance.check_in:
                attendance.video_base64 =self.env['attendance.video'].search([['attendance_id','=',attendance.id]]).checkin_video

            else:
                attendance.video_base64 = False
    @api.depends('check_out')
    def get_html_checkout(self):
        for attendance in self:
            if attendance.video_base64_checkout != False:
                attendance.tracking_video_checkout = f'<video width="320" height="240" controls=""><source src="data:video/mp4;base64,{ attendance.video_base64_checkout }" type="video/mp4"/></video>'
            else:
                attendance.tracking_video_checkout =f'<field name="video_base64_checkout"/>'
    @api.depends('check_out')
    def _compute_video_base64_checkout(self):
        for attendance in self:
            if attendance.check_out:
                attendance.video_base64_checkout =self.env['attendance.video'].search([['attendance_id','=',attendance.id]]).checkout_video
            else:
                attendance.video_base64_checkout = False