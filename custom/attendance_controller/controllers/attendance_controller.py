# -*- coding: utf-8 -*-
from odoo import exceptions, http
from odoo.http import request, Response
import json
from collections import defaultdict
from datetime import datetime, timedelta
from operator import itemgetter
import socket
from pytz import timezone
from datetime import datetime
from odoo.tools.json import JSON


class AttendanceController(http.Controller):
    def get_currenttime(self):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        return dt_string

    def setTimezone(self, datetime):
        zone = timezone('Asia/Ho_Chi_Minh')
        time_correct = datetime.astimezone(zone)
        return time_correct

    @http.route('/attendance_controller/employee_all', auth='public', csrf=False)
    def index(self, **kw):
        employees_rec = http.request.env['hr.employee'].search([])
        output = "<h1>The list of employees: </h1><ul>"
        for employee in employees_rec:
            output += '<li>' + employee['name'] + '</li>' + '/<ul>'
        return output

    @http.route('/attendance_controller/employee-RFID-Exist/<string:rfid>', auth='public', type='http', csrf=False)
    def get_employee_by_rfid_exist(self, rfid, **kw):
        employee_rfid = http.request.env['hr.employee'].sudo().search([["x_EMPLOYEE_RFID", "=", rfid]])
        print(employee_rfid['id'])
        last_checkin = http.request.env['hr.attendance'].sudo().search([["employee_id", "=", employee_rfid.id]])
        print(last_checkin)
        if len(last_checkin) != 0 and employee_rfid.name is not False:
            if last_checkin[0].check_in is not False and last_checkin[0].check_out is False:
                vals = {
                    "signalexist": "exist",
                    "signalcheck": "checkout"

                }
            else:
                vals = {
                    "signalexist": "exist",
                    "signalcheck": "checkin"

                }
        elif len(last_checkin) == 0 and employee_rfid.name is not False:
            vals = {
                "signalexist": "exist",
                "signalcheck": "checkin"

            }
        else:
            vals = {
                "signalexist": "not exist",
                "signalcheck": "can't check"
            }

        return Response(json.dumps(vals, ensure_ascii=False))

    # api get employee information
    @http.route('/attendance_controller/employee-RFID/<string:rfid>', auth='public', type='http', csrf=False)
    def get_employee_by_rfid(self, rfid, **kw):
        employee_rfid = http.request.env['hr.employee'].sudo().search([["x_EMPLOYEE_RFID", "=", rfid]])
        last_checkin = http.request.env['hr.attendance'].sudo().search([["employee_id", "=", employee_rfid['id']]])
        name = employee_rfid['name']
        department = http.request.env['hr.department'].sudo().search([["id", "=", int(employee_rfid['department_id'])]])
        if len(last_checkin) == 0:
            print("1")
            data = {
                "id": employee_rfid['pin'],
                "name": name,
                "work phone": employee_rfid['work_phone'],
                "work email": employee_rfid['work_email'],
                "job": employee_rfid['job_title'],
                "department": department['name'],
                "avatar": str(employee_rfid['image_1920']),
            }
        elif len(last_checkin) < 2:
            print("2")

            data = {
                "id": employee_rfid['pin'],
                "name": name,
                "work phone": employee_rfid['work_phone'],
                "work email": employee_rfid['work_email'],
                "job": employee_rfid['job_title'],
                "department": department['name'],
                "avatar": str(employee_rfid['image_1920']),
                "last_checkin": "False",
                "last_checkin_image": "False",
                "last_checkout": "False",
                "last_checkout_image": "False",
                "checkin": str(self.setTimezone(last_checkin[0]['check_in'])),
                "checkin_image": str(last_checkin[0].checkin_image),
                "gender": employee_rfid["gender"],
            }
        else:
            print("3")

            if last_checkin[0].check_out:
                print("4")

                data = {
                    "id": employee_rfid['pin'],
                    "name": name,
                    "work phone": employee_rfid['work_phone'],
                    "work email": employee_rfid['work_email'],
                    "job": employee_rfid['job_title'],
                    "department": department['name'],
                    "avatar": str(employee_rfid['image_1920']),
                    "last_checkout": str(self.setTimezone(last_checkin[1].check_out)),
                    "last_checkout_image": str(last_checkin[1].checkout_image),
                    "last_checkin": str(self.setTimezone(last_checkin[1]['check_in'])),
                    "last_checkin_image": str(last_checkin[1].checkin_image),
                    "checkin": str(self.setTimezone(last_checkin[0]['check_in'])),
                    "checkin_image": str(last_checkin[0].checkin_image),
                    "gender": employee_rfid["gender"],
                }
            elif last_checkin[0].check_out is not False:
                print("5")

                data = {
                    "id": employee_rfid['pin'],
                    "name": name,
                    "work phone": employee_rfid['work_phone'],
                    "work email": employee_rfid['work_email'],
                    "job": employee_rfid['job_title'],
                    "department": department['name'],
                    "avatar": str(employee_rfid['image_1920']),
                    "last_checkin": str(self.setTimezone(last_checkin[1]['check_in'])),
                    "last_checkin_image": str(last_checkin[1].checkin_image),
                    "last_checkout": str(self.setTimezone(last_checkin[1].check_out)),
                    "last_checkout_image": str(last_checkin[1].checkout_image),
                    "checkin": str(self.setTimezone(last_checkin[0]['check_in'])),
                    "checkin_image": str(last_checkin[0].checkin_image),
                    "gender": employee_rfid["gender"],
                }
            else:
                print("6")

                data = {
                    "id": employee_rfid['pin'],
                    "name": name,
                    "work phone": employee_rfid['work_phone'],
                    "work email": employee_rfid['work_email'],
                    "job": employee_rfid['job_title'],
                    "department": department['name'],
                    "avatar": str(employee_rfid['image_1920']),
                    "last_checkin": str(self.setTimezone(last_checkin[1]['check_in'])),
                    "last_checkin_image": str(last_checkin[1].checkin_image),
                    "last_checkout": str(self.setTimezone(last_checkin[1].check_out)),
                    "last_checkout_image": str(last_checkin[1].checkout_image),
                    "checkin": str(self.setTimezone(last_checkin[0]['check_in'])),
                    "checkin_image": str(last_checkin[0].checkin_image),
                    "gender": employee_rfid["gender"],
                }
        return Response(json.dumps(data, ensure_ascii=False))

    # api checkin
    @http.route('/attendance_controller/employee-checkin', type='json', auth='public',
                methods=['POST'], cors='*', csrf=False)
    def get_employee_checkin(self, **rec):
        print("checkin")
        employee_request = json.loads(request.httprequest.data)
        if employee_request is not None:
            employee_rfid = http.request.env['hr.employee'].sudo().search(
                [["x_EMPLOYEE_RFID", "=", employee_request['rfid']]])
            print(employee_rfid['gender'])
            image_request = employee_request['image']
            checkin_request = self.get_currenttime()
            print(checkin_request)
            if employee_request['rfid'] == " ":
                raise exceptions.ValidationError("RFID is empty")
            if employee_rfid:
                vals = {
                    'employee_id': employee_rfid['id'],
                    'check_in': str(checkin_request),
                    'checkin_image': str(image_request),
                }
                employee_attendance = http.request.env['hr.attendance'].sudo().create(vals)
                return {
                    "code": 201,
                    "message": 'Successfully Check-in',
                    'check in image': str(image_request),
                    "gender": employee_rfid['gender']
                }
            else:
                raise exceptions.ValidationError("Can not find employee")
        else:
            raise exceptions.ValidationError('Invalid Employee Input')

    # api checkout

    @http.route('/attendance_controller/employee-checkout', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def get_employee_checkout(self, **rec):
        employee_request = json.loads(request.httprequest.data)
        if employee_request is not None:
            # print(str(employee_request['image']))
            # print(employee_request['checkout_time'])
            employee_rfid = http.request.env['hr.employee'].sudo().search(
                [["x_EMPLOYEE_RFID", "=", employee_request['rfid']]])
            if employee_rfid:
                employee_id = employee_rfid['id']
                employee_attendance = http.request.env['hr.attendance'].sudo().search(
                    [("employee_id", "=", employee_id), ("check_out", '=', False)], order='check_in desc')
                if not employee_attendance:
                    raise exceptions.ValidationError("Employee already checked-out or has not checked-in yet")
                else:
                    flag = employee_attendance[0]
                    if flag is not None:
                        vals = {
                            'check_out': str(self.get_currenttime()),
                            'checkout_image': str(employee_request['image'])
                        }
                        if not flag['check_out']:
                            flag.sudo().write(vals)
                            return {
                                "code": 201,
                                "message": 'Successfully Check-out',
                                'time checkout': str(self.get_currenttime()),
                                'checkout image': employee_request['image'],
                                "gender": employee_rfid['gender']

                            }
                        else:
                            raise exceptions.ValidationError("Employee is already checked-out")
            else:
                raise exceptions.ValidationError("Can not find employee")
        else:
            raise exceptions.ValidationError("Invalid Employee Input")

    @http.route('/attendance_controller/create_new_hr_employee', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def create_new_hr_employee(self, **rec):
        employee_request = json.loads(request.httprequest.data)
        if employee_request is not None:
            id = employee_request["id"]
            rfid = employee_request["rfid"]
            employee_info = http.request.env['hr.employee'].sudo().search([["pin", "=", id]])
            if not employee_info:
                raise exceptions.ValidationError("ID does not exist")
            else:
                if employee_info['x_EMPLOYEE_RFID'] is False or employee_info['x_EMPLOYEE_RFID'] == "":
                    vals = {
                        "x_EMPLOYEE_RFID": rfid
                    }
                    employee_info.sudo().write(vals)
                    return {
                        "code": 201,
                        "message": 'Successfully',
                        "name": employee_info['name']
                    }
                else:
                    raise exceptions.ValidationError("EMPLOYEE HAVE RFID")

        else:
            raise exceptions.ValidationError("Invalid Employee Input")

    @http.route('/attendance_controller/show_information_employee_by_id/<string:id>', auth='public', type='http',
                csrf=False)
    def show_information_employee_by_id(self, id, **aw):
        employee_info = http.request.env['hr.employee'].sudo().search([["pin", "=", id]])
        department = http.request.env['hr.department'].sudo().search([["id", "=", int(employee_info['department_id'])]])
        if not employee_info:
            vals = {
                "code": "ID is not exist",
                "name": "false",
                "ID": "false",
                "department": "false",
                "avatar": "false",
                "phone": "false",

            }
        else:
            if employee_info['x_EMPLOYEE_RFID'] is False or employee_info['x_EMPLOYEE_RFID'] == "":
                vals = {
                    "code": "ok",
                    "name": employee_info['name'],
                    "ID": employee_info['pin'],
                    "department": department['name'],
                    "avatar": str(employee_info['image_1920']),
                    "phone": employee_info['work_phone'],

                }

            else:
                vals = {
                    "code": "Employee had RFID ",
                    "name": "false",
                    "ID": "false",
                    "department": "false",
                    "avatar": "false",
                    "phone": "false",
                }
        return Response(json.dumps(vals, ensure_ascii=False))

    @http.route('/attendence_controller/update_checkout', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def Update_checkout(self, **rec):
        data_request = json.loads(request.httprequest.data)
        if data_request is not None:
            employee_rfid = http.request.env['hr.employee'].sudo().search(
                [["x_EMPLOYEE_RFID", "=", data_request['rfid']]])
            if employee_rfid:
                employee_id = employee_rfid['id']
                employee_attendance = http.request.env['hr.attendance'].sudo().search(
                    [["employee_id", "=", employee_id]])
                print(employee_attendance[0]['check_out'])
                vals = {
                    'check_out': str(self.get_currenttime()),
                    'checkout_image': str(data_request['image'])
                }
                employee_attendance[0].sudo().write(vals)
                return {
                    "code": 201,
                    "message": 'Successfully Check-out',
                    'time checkout': str(self.get_currenttime()),
                    'checkout image': data_request['image'],
                    "gender": employee_rfid['gender']

                }
            else:
                raise exceptions.ValidationError("Can not find employee")
        else:
            raise exceptions.ValidationError("Invalid Employee Input")

    @http.route('/attendence_controller/update_forget_checkout', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def update_forget_checkout(self, **rec):
        data_request = json.loads(request.httprequest.data)
        if data_request is not None:
            employee_rfid = http.request.env['hr.employee'].sudo().search(
                [["x_EMPLOYEE_RFID", "=", data_request['rfid']]])
            if employee_rfid:
                employee_id = employee_rfid['id']
                employee_attendance = http.request.env['hr.attendance'].sudo().search(
                    [["employee_id", "=", employee_id]])
                vals = {
                    'check_out': employee_attendance[0]['check_in'],
                }
                employee_attendance[0].sudo().write(vals)
                return {
                    "code": 201,
                    "message": 'Successfully Check-out',
                }
            else:
                raise exceptions.ValidationError("Can not find employee")
        else:
            raise exceptions.ValidationError("Invalid Employee Input")

    @http.route('/attendance_controller/get_time_checkin/<string:rfid>', auth='public', type='http', csrf=False)
    def get_time_checkin(self, rfid, **kw):
        employee_rfid = http.request.env['hr.employee'].sudo().search([["x_EMPLOYEE_RFID", "=", rfid]])
        print(employee_rfid['id'])
        if employee_rfid:
            last_checkin = http.request.env['hr.attendance'].sudo().search([["employee_id", "=", employee_rfid.id]])
            if last_checkin:
                time_user_checkin = self.setTimezone(last_checkin[0]['check_in'])
                if time_user_checkin.date() == datetime.now().date():

                    return str(time_user_checkin.time())
                else:

                    return "false"
            else:
                return "false"
        else:
            return "false"

    @http.route('/attendance_controller/get_time_checkout/<string:rfid>', auth='public', type='http', csrf=False)
    def get_time_checkout(self, rfid, **kw):
        try:
            employee_rfid = http.request.env['hr.employee'].sudo().search([["x_EMPLOYEE_RFID", "=", rfid]])
            if employee_rfid:
                last_checkout = http.request.env['hr.attendance'].sudo().search([["employee_id", "=", employee_rfid.id]])
                if last_checkout[0]['check_out']:
                    time_user_checkout = self.setTimezone(last_checkout[0]['check_out'])
                    if time_user_checkout.date() == datetime.now().date():
                        return str(time_user_checkout.time())
                    else:
                        return "false"
                else:
                    return "false"
            else:
                return "false"
        except Exception as e:
            return {
                "code": 200,
                "status": "Error",
                "message": e
            }

    @http.route('/attendance_controller/add_new_video_checkin', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def update_video(self, **rec):
        try:
            data_request = json.loads(request.httprequest.data)
            if data_request is None:
                raise exceptions.ValidationError("Invalid input")
            else:
                id_employee_rfid = http.request.env['hr.employee'].sudo().search(
                    [["x_EMPLOYEE_RFID", "=", data_request['rfid']]])
                print(id_employee_rfid)
                if id_employee_rfid:
                    last_checkin = http.request.env['hr.attendance'].sudo().search(
                        [["employee_id", "=", id_employee_rfid.id]])
                    print(last_checkin[0])
                    if (last_checkin[0]['check_in']) and (data_request['checkin_video'] != "False"):
                        time_user_checkout = self.setTimezone(last_checkin[0]['check_in'])
                        if time_user_checkout.date() == datetime.now().date():
                            vals = {
                                "attendance_id": last_checkin[0].id,
                                "checkin_video": data_request['checkin_video'],
                                "employee_id": id_employee_rfid.id
                            }
                            data = {
                                "code": 201,
                                "status": "Succesfully",
                            }
                            http.request.env['attendance.video'].sudo().create(vals)
                            return data
                        else:
                            raise exceptions.ValidationError("RFID not checkin today ")
                    else:
                        raise exceptions.ValidationError("RFID not checkin")
                else:
                    raise exceptions.ValidationError("Don't have RFID")
        except Exception as e:
            return {
                "code": 200,
                "status": "Error",
                "message": e
            }
    @http.route('/attendance_controller/add_new_video_checkout', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def update_video_checkout(self, **rec):
        try:
            data_request = json.loads(request.httprequest.data)
            if data_request is None:
                raise exceptions.ValidationError("Invalid input")
            else:
                id_employee_rfid = http.request.env['hr.employee'].sudo().search(
                    [["x_EMPLOYEE_RFID", "=", data_request['rfid']]])
                if id_employee_rfid:
                    last_checkin = http.request.env['hr.attendance'].sudo().search(
                        [["employee_id", "=", id_employee_rfid.id]])
                    if (last_checkin[0]['check_out']) and (data_request['checkout_video'] != "False"):
                        time_user_checkout = self.setTimezone(last_checkin[0]['check_out'])
                        if time_user_checkout.date() == datetime.now().date():
                            exits = http.request.env['attendance.video'].sudo().search([["attendance_id", "=", last_checkin[0].id]])
                            if exits['checkout_video'] is False or exits['checkout_video'] == "":
                                vals = {
                                    "checkout_video": data_request['checkout_video'],
                                }
                                exits.sudo().write(vals)
                                data = {
                                    "code": 201,
                                    "status": "Succesfully",
                                }
                            return data
                        else:
                            raise exceptions.ValidationError("RFID not checkin today ")
                    else:
                        raise exceptions.ValidationError("RFID not checkin")
                else:
                    raise exceptions.ValidationError("Don't have RFID")
        except Exception as e:
            return {
                "code": 200,
                "status": "Error",
                "message": e
            }