# -*- coding: utf-8 -*-
# from odoo import http


# class PosTotalQuantityCustom(http.Controller):
#     @http.route('/pos_total_quantity_custom/pos_total_quantity_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_total_quantity_custom/pos_total_quantity_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_total_quantity_custom.listing', {
#             'root': '/pos_total_quantity_custom/pos_total_quantity_custom',
#             'objects': http.request.env['pos_total_quantity_custom.pos_total_quantity_custom'].search([]),
#         })

#     @http.route('/pos_total_quantity_custom/pos_total_quantity_custom/objects/<model("pos_total_quantity_custom.pos_total_quantity_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_total_quantity_custom.object', {
#             'object': obj
#         })
