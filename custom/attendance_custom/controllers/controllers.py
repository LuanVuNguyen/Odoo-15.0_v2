# -*- coding: utf-8 -*-
# from odoo import http


# class AttendanceCustom(http.Controller):
#     @http.route('/attendance_custom/attendance_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attendance_custom/attendance_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('attendance_custom.listing', {
#             'root': '/attendance_custom/attendance_custom',
#             'objects': http.request.env['attendance_custom.attendance_custom'].search([]),
#         })

#     @http.route('/attendance_custom/attendance_custom/objects/<model("attendance_custom.attendance_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attendance_custom.object', {
#             'object': obj
#         })
