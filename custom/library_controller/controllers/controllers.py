# -*- coding: utf-8 -*-
# from odoo import http

from datetime import datetime

from odoo import exceptions, http
from odoo.http import request, Response
import re
import json
import csv
import logging
import os.path
import base64
from datetime import datetime

from stdnum.cr import cr

current_Date = datetime.today().strftime('%m/%d/%Y')


class LibraryController(http.Controller):

    # def create_new_inventory_record(self, data_read, rfidHad):
    #     for line in data_read:
    #         if line["rfid"] not in rfidHad:
    #             rfid = line["rfid"]
    #             quantity = line["quantity"]
    #             product_id = http.request.env['product.template'].sudo().search([['x_RFID_PRODUCT', '=', rfid]])
    #             product_product_id = http.request.env['product.product'].sudo().search(
    #                 [('product_tmpl_id', '=', product_id['id'])])
    #             date = datetime.strptime("12/31/2022", '%m/%d/%Y')
    #             print(product_id)
    #             vals1 = {
    #                 "product_id": product_product_id.id,
    #                 "inventory_quantity": quantity,
    #                 "inventory_diff_quantity": quantity,
    #                 "inventory_quantity_set": True,
    #                 "location_id": 8,
    #                 "company_id": 1
    #             }
    #             http.request.env['stock.quant'].sudo().create(vals1)
    #
    # def fill_record(self, member, book):
    #     date = datetime.strptime("12/21/2022", '%m/%d/%Y')
    #     partner_id = http.request.env['res.partner'].sudo().search([('x_Member_RFID', '=', member)])
    #     book_id = http.request.env['product.product'].sudo().search([('x_RFID_PRODUCT', '=', book)])
    #     vals = {
    #         "register_book_name": book_id.id,
    #         "register_author_name": book_id.author_name,
    #         "register_book_title": book_id.book_title,
    #         "register_isbn_number": book_id.isbn_number,
    #         "register_isbn_13_number": book_id.isbn_13_number,
    #         "book_image": book_id.image_1920,
    #         "register_edition": book_id.edition,
    #         "calc_return_date": date,
    #         "register_member": partner_id.id,
    #         "register_member_id": partner_id["member_sequence"]
    #     }
    #     return vals
    #
    # @http.route('/library_controller/get_book', type='json', auth='public')
    # def get_book(self):
    #     request_data = json.loads(request.httprequest.data)
    #     print(request_data)
    #     if request_data is not None:
    #         print(request_data)
    #         rfid = request_data['rfid']
    #         value = []
    #         err_RFID = []
    #         for v in rfid:
    #             product_templ_id = http.request.env['product.template'].sudo().search([['x_RFID_PRODUCT', '=', v]])
    #             author = product_templ_id['author_name']
    #             authors = ""
    #             for a in range(len(author)):
    #                 authors += author[a]['author_name']
    #                 if a > 0:
    #                     authors += ", " + author[a]['author_name']
    #             vals = {
    #                 "RFID": product_templ_id['x_RFID_PRODUCT'],
    #                 "Book_title": product_templ_id['book_title'],
    #                 "ISBN_13": product_templ_id['isbn_13_number'],
    #                 "Author": authors,
    #                 "Categories": product_templ_id['categories']
    #             }
    #             if vals['Book_title'] is not False:
    #                 value.append(vals)
    #         values = {"Type": "Product_Card",
    #                   "content": value
    #                   }
    #         return values
    #
    # @http.route('/library_controller/get_member', type='json', auth='public')
    # def get_member(self):
    #     request_data = json.loads(request.httprequest.data)
    #     print(request_data)
    #     if request_data is not None:
    #         rfid = request_data['rfid']
    #         print(rfid)
    #         value = []
    #         v = rfid[0]
    #         member_templ_id = http.request.env['res.partner'].sudo().search([['x_Member_RFID', '=', v]])
    #         print(member_templ_id)
    #         membership_type = member_templ_id["membership_type"]
    #         country = member_templ_id["country_id"]
    #         vals = {
    #             "Type": "Member_Card",
    #             "content": {
    #                 "RFID": member_templ_id['x_Member_RFID'],
    #                 "Name": member_templ_id["name"],
    #                 "Member_ID": member_templ_id["member_sequence"],
    #                 "Gender": member_templ_id["sex"],
    #                 "Current_membership": membership_type["membership_name"],
    #                 "Contact": member_templ_id["street"],
    #             }
    #         }
    #     return vals
    #
    # @http.route('/library_controller/issue', auth='public', type='json', methods=['POST'], cors='*', csrf=False)
    # def issueBook(self, **kwargs):
    #     request_data = json.loads(request.httprequest.data)
    #     print(request_data)
    #     if request_data is not None:
    #         member = request_data['member']
    #         books = request_data['books']
    #         for i in books:
    #             vals = self.fill_record(member, i)
    #             http.request.env['book.register'].sudo().create(vals)
    #     args = {'success': True, 'message': 'Success'}
    #     return args

    # SCAN RFID

#API SCAN KIEM KE
    @http.route('/inventory_controller/get_quant', type='json', auth='public')
    def get_multiple_product(self):
        try:
            request_data = json.loads(request.httprequest.data)
            if request_data is not None:
                rfid = request_data['rfid']
                value = []
                err_RFID = []
                for v in rfid:
                    product_templ_id = http.request.env['product.template'].sudo().search([['x_RFID_PRODUCT', '=', v]])
                    vals = {
                        "RFID": product_templ_id['x_RFID_PRODUCT'],
                        "Product_name": product_templ_id['name'],
                        "Product_code": product_templ_id['barcode'],
                        "quantity": 1,
                    }
                    if vals['Product_name'] is not False:
                        value.append(vals)
                    else:
                        err_RFID.append(v)
            return value, err_RFID
        except Exception as e:
            return {
                "status": "Error",
                "code": 200,
                "message": e
            }

    # API LUU FILE CVS
    @http.route('/inventory_controller/create_fileinventory', auth='public', methods=['POST'], type='json', cors='*',
                csrf=False)
    def create_inventory(self, **kwargs):
        try:
            request_data = json.loads(request.httprequest.data)
            print(request_data)
            if request_data is not None:
                data_get = base64.b64decode(request_data['base64']).decode("UTF-8")
                data_get_split = data_get.replace('"', '').split('\n')
                list_data_get = [x.split(",") for x in data_get_split]
                data = []
                for i in range(1, len(list_data_get) - 1):
                    data.append(self.create_dict(list_data_get[0], list_data_get[i]))
            print(data)
            rfidHad = []
            for line in data:
                rfid = line['rfid'],
                # barcode = line['barcode'],
                # product = line['product_name'],
                quantity = line['quantity'],

                product_id = http.request.env['product.template'].sudo().search([['x_RFID_PRODUCT', '=', rfid]])

                product_product_id = http.request.env['product.product'].sudo().search(
                    [('product_tmpl_id', '=', product_id['id'])])

                stock_id = http.request.env['stock.quant'].sudo().search(
                    [("product_id", "=", product_product_id['id'])])

                if (http.request.env['stock.quant'].sudo().search([("product_id", "=", product_product_id['id'])])):
                    vals = {
                        'inventory_quantity': quantity[0]
                    }
                    rfidHad.append(line['rfid'])
                    for value in stock_id:
                        value.sudo().write(vals)
            print( )
            print(rfidHad)
            self.create_new_inventory_record(data, rfidHad)
            return Response(json.dumps(json.dumps({
                "code": 201,
                "message": 'Successfully Update Product Quantity', })))
        except Exception as e:
            return {
                "code": 200,
                "message": e
            }
    def create_dict(self, keydict, valuedict):
        try:
            res = {}
            for key in keydict:
                for value in valuedict:
                    res[key] = value
                    valuedict.remove(value)
                    break
            return res
        except Exception as e:
            return e

    # HIỂN THỊ THÔNG TIN SẢN PHẦM
    @http.route('/inventory_controller/get_info_product', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def get_info_product(self, **rec):
        try:
            product_request = json.loads(request.httprequest.data)
            if product_request is None:
                raise exceptions.ValidationError("INPUT ERROR, PLEASE CHECK AGAIN")
            else:
                pincode = product_request["barcode"]
                product_request = http.request.env['product.template'].sudo().search([["barcode", "=", pincode]])
                if not product_request:
                    raise exceptions.ValidationError("PINCODE IS NOT EXIST")
                else:
                    # Chuyen doi chuoi id thanh so
                    user_id = re.sub(r'\D', '', str(product_request['responsible_id']))
                    categ_id = re.sub(r'\D', '', str(product_request['categ_id']))
                    # đặt điều kiện cho users_id nếu sản phẩm không có nguoi dùng thì users_id=0
                    if user_id == '':
                        user_id = 0
                    else:
                        # request id
                        users_info = http.request.env['res.users'].sudo().search([['id', '=', int(user_id)]])
                        categ_info = http.request.env['product.category'].sudo().search([['id', '=', int(categ_id)]])
                        vals = {
                            "code": 201,
                            "status": "SUCCESSFULLY",
                            "RFID": product_request['x_RFID_PRODUCT'],
                            "Pin Code": pincode,
                            "Name Product": product_request['name'],
                            "Product Category": categ_info['complete_name'],
                            "Responsible": users_info['name']
                        }
                        return vals
        except Exception as e:
            return {
                "code": 200,
                "status": "Error",
                "message": e
            }

    # API DANG KI RFID CHO SAN PHAM THEO MA PIN
    @http.route('/inventory_controller/register_product', type='json', auth='public', methods=['POST'], cors='*',
                csrf=False)
    def create_new_product(self, **rec):
        try:
            product_request = json.loads(request.httprequest.data)
            if product_request is not None:
                pin = product_request["barcode"]
                rfid = product_request["rfid"]
                product_request = http.request.env['product.template'].sudo().search([["barcode", "=", pin]])
                if not product_request:
                    raise exceptions.ValidationError("PINCODE DOES NOT EXIST")
                else:
                    if product_request['x_RFID_PRODUCT'] is False or product_request['x_RFID_PRODUCT'] == "":
                        vals = {
                            "x_RFID_PRODUCT": rfid
                        }
                        product_request.sudo().write(vals)
                        return {
                            "code": 201,
                            "message": 'Successfully'
                        }
                    else:
                        raise exceptions.ValidationError("PRODUCT HAVED RFID")
            else:
                raise exceptions.ValidationError("Invalid Product Input")
        except Exception as e:
            return {
                "code": 200,
                "message": e
            }

    # API DANG KI SAN PHAM MOI
    @http.route('/inventory_controller/creat_new_product', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def creat_new_product(selfs, **rec):
        try:
            product_resquest = json.loads(request.httprequest.data)
            if product_resquest:
                responsible = product_resquest['responsible']
                name_product = product_resquest['name_product']
                pin = product_resquest["barcode"]
                rfid = product_resquest["rfid"]
                users_info = http.request.env['res.users'].sudo().search([['name', '=', responsible]])
                product_resquest = http.request.env['product.template'].sudo().search([["barcode", "=", pin]])
                product_resquest_rfid = http.request.env['product.template'].sudo().search(
                    [["x_RFID_PRODUCT", "=", rfid]])
                if not users_info:
                    raise exceptions.ValidationError("USERS IS NOT EXISTED")
                elif product_resquest:
                    raise exceptions.ValidationError("PINCODE PRODUCT IS EXISTED")
                elif product_resquest_rfid:
                    raise exceptions.ValidationError("RFID PRODUCT IS EXISTED")
                else:
                    print(users_info['id'])
                    vals = {
                        "responsible_id": users_info['id'],
                        "x_RFID_PRODUCT": rfid,
                        "barcode": pin,
                        "name": name_product
                    }
                    print(vals)
                    http.request.env['product.template'].sudo().create(vals)
                    return {
                        "code": 201,
                        "message": 'Successfully',
                    }
            else:
                raise exceptions.ValidationError("Invalid Product Input")
        except Exception as e:
            return {
                "status": 200,
                "message": e
            }
