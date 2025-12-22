from odoo import api, fields, models,_
from odoo.exceptions import ValidationError



class StockLine(models.Model):
    _inherit='stock.move.line'
    qty_available = fields.Float(string="Quantity On Hand",compute='_calc_qty_available',store=True)
    ore_id = fields.Many2one(comodel_name="product.ore", string="نوع الخامة", related='product_id.ore_id',store=True)
    session_id = fields.Many2one(comodel_name="product.session", string="الموسم",related='product_id.session_id',store=True)
    categ_id = fields.Many2one(comodel_name="product.category", string="Category",related='product_id.categ_id',store=True)
    color = fields.Char(string='Color',related='product_id.color',store=True)
    size = fields.Char(string='Size',related='product_id.size',store=True)
    model_year = fields.Char(string='Model Year', related='product_id.model_year',store=True)


    @api.depends('product_id.qty_available','picking_id.location_id')
    def _calc_qty_available(self):
        for line in self:
            inventory_quant = self.env['stock.quant'].search([
                ('location_id', '=', line.picking_id.location_id.id),
                ('product_id', '=',  line.product_id.id)
            ])
            qty_available=sum(inventory_quant.mapped('quantity'))
            line.qty_available = qty_available if qty_available>0 else 0

    @api.onchange('product_id')
    def onchange_product_id555(self):
        self.qty_done = 1



    @api.constrains('qty_done','picking_id.location_id')
    def check_qty_done_hand(self):
        for line in self:
            if line.picking_id:
                if line.picking_id.picking_type_code in ('outgoing','internal'):
                    inventory_quant = self.env['stock.quant'].search([
                        ('location_id', '=', line.picking_id.location_id.id),
                        ('product_id', '=', line.product_id.id)
                    ])
                    qty_available=sum(inventory_quant.mapped('quantity'))
                    # if line.qty_done>qty_available:
                    #     raise ValidationError("Order Qty Greater Than  Qtuantity On Hand")
#
# class Stock(models.Model):
#     _inherit='stock.move'
#
#
#     @api.constrains('quantity_done')
#     def check_qty_done_hand(self):
#         for line in self:
#             if line.picking_id:
#                 if line.picking_id.picking_type_code=='outgoing':
#                     if line.quantity_done>line.product_id.qty_available:
#                         raise ValidationError("Order Qty Greater Than  Qtuantity On Hand")

class Quant(models.Model):
    _inherit='stock.quant'
    barcode2 = fields.Char(string="Barcode",compute='_calc_barcode',search='_search_barcode',store=False)
    product_template_attribute_value_ids = fields.Many2many(related='product_id.product_template_attribute_value_ids', readonly=True)
    ore_id = fields.Many2one(comodel_name="product.ore", string="نوع الخامة", related='product_id.ore_id',store=True)
    session_id = fields.Many2one(comodel_name="product.session", string="الموسم",related='product_id.session_id',store=True)
    categ_id = fields.Many2one(comodel_name="product.category", string="Category",related='product_id.categ_id',store=True)
    color = fields.Char(string='Color',related='product_id.color',store=True)
    size = fields.Char(string='Size',related='product_id.size',store=True)
    model_year = fields.Char(string='Model Year', related='product_id.model_year',store=True)

    list_price = fields.Float(related='product_id.list_price',store=True)
    standard_price = fields.Float(related='product_id.standard_price',store=True)
    virtual_available = fields.Float(related='product_id.virtual_available',store=True)
    product_tmpl_id2 = fields.Many2one('product.template', string='Product Template',related='product_id.product_tmpl_id',store=True)



    @api.depends('product_id')
    def _calc_barcode(self):
       for rec in self:
           rec.barcode2=rec.product_id.barcode

    def _search_barcode(self, operator, value):

        product_temp=self.env['product.product'].search([('barcode','=',value)],limit=1)
        if product_temp:
            return [('product_tmpl_id' ,'=', product_temp.product_tmpl_id.id)]
        else:
            return []

    @api.model
    def action_view_quants2(self):
        self = self.with_context(search_default_internal_loc=1)
        self = self._set_view_context()
        return self._get_quants_action2(extend=True)

    @api.model
    def _get_quants_action2(self, domain=None, extend=False):
        """ Returns an action to open (non-inventory adjustment) quant view.
        Depending of the context (user have right to be inventory mode or not),
        the list view will be editable or readonly.

        :param domain: List for the domain, empty by default.
        :param extend: If True, enables form, graph and pivot views. False by default.
        """
        self._quant_tasks()
        ctx = dict(self.env.context or {})
        ctx['inventory_report_mode'] = True
        ctx.pop('group_by', None)
        action = {
            'name': _('Stock On Hand'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'stock.quant',
            'type': 'ir.actions.act_window',
            'context': ctx,
            'domain': domain or [],
            'help': """
                 <p class="o_view_nocontent_empty_folder">No Stock On Hand</p>
                 <p>This analysis gives you an overview of the current stock
                 level of your products.</p>
                 """
        }

        target_action = self.env.ref('stock.dashboard_open_quants', False)
        if target_action:
            action['id'] = target_action.id

        form_view = self.env.ref('stock.view_stock_quant_form_editable').id
        if self.env.context.get('inventory_mode') and self.user_has_groups('stock.group_stock_manager'):
            action['view_id'] = self.env.ref('stock.view_stock_quant_tree_editable').id
        else:
            action['view_id'] = self.env.ref('stock.view_stock_quant_tree').id
        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })
        if extend:
            action.update({
                'view_mode': 'tree,form,pivot,graph',
                'views': [
                    (self.env.ref('project_custom.view_stock_quant_tree_inventory_editable2').id, 'list'),
                    (form_view, 'form'),
                    (self.env.ref('stock.view_stock_quant_pivot').id, 'pivot'),
                    (self.env.ref('stock.stock_quant_view_graph').id, 'graph'),
                ],
            })
        return action

