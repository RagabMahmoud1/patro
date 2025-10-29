# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = "product.template"
    vendors = fields.Char(string='Vendors', compute='_compute_vendors')
    model = fields.Char(string='Model', required=False)

    @api.depends('seller_ids', 'seller_ids.name', 'seller_ids.name.name')
    def _compute_vendors(self):
        for rec in self:
            partner_names = rec.seller_ids.mapped('name.name')
            rec.vendors = ', '.join(partner_names)

class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    # Additional measures
    cost_total = fields.Float(string='Cost Total', readonly=True)
    cost_avg = fields.Float(string='Cost Avg', readonly=True, group_operator="avg")
    qty_available = fields.Float(string='On Hand', readonly=True, group_operator="sum")
    model = fields.Char(string='Model', readonly=True)
    vendors_names = fields.Char(string='Vendors', readonly=True)

    def _select(self):
        select_str = super(PosOrderReport, self)._select()
        # Add cost (from l.total_cost) and on hand to SELECT
        select_str += """,
                SUM(ROUND((COALESCE(l.total_cost, 0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END), cu.decimal_places)) AS cost_total,
                CASE
                    WHEN SUM(l.qty * u.factor) = 0 THEN NULL
                    ELSE (SUM(COALESCE(l.total_cost, 0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) / SUM(l.qty * u.factor))::decimal
                END AS cost_avg,
                MAX(COALESCE(q.qty_available, 0)) AS qty_available,
                pt.model AS model,
                COALESCE(MAX(v.vendors_names), '') AS vendors_names
        """
        return select_str

    def _group_by(self):
        group_str = super(PosOrderReport, self)._group_by()
        # Add pt.model only (vendors_names is aggregated via string_agg)
        return group_str + ", pt.model"

    def _from(self):
        from_str = super(PosOrderReport, self)._from()
        # Join aggregated stock quantities per product to avoid correlated subquery and grouping errors
        from_str += """
                LEFT JOIN (
                    SELECT sq.product_id, SUM(sq.quantity) AS qty_available
                    FROM stock_quant sq
                    JOIN stock_location sl ON sl.id = sq.location_id
                    WHERE sl.usage = 'internal'
                    GROUP BY sq.product_id
                ) AS q ON q.product_id = p.id
                LEFT JOIN (
                    SELECT psi.product_tmpl_id, string_agg(DISTINCT rp.name, ', ') AS vendors_names
                    FROM product_supplierinfo psi
                    JOIN res_partner rp ON rp.id = psi.name
                    GROUP BY psi.product_tmpl_id
                ) AS v ON v.product_tmpl_id = pt.id
        """
        return from_str


