# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    # Additional measures
    cost_total = fields.Float(string='Cost Total', readonly=True)
    cost_avg = fields.Float(string='Cost Avg', readonly=True, group_operator="avg")
    qty_available = fields.Float(string='On Hand', readonly=True, group_operator="avg")

    def _select(self):
        select_str = super(PosOrderReport, self)._select()
        # Add cost (from l.total_cost) and on hand to SELECT
        select_str += """,
                SUM(COALESCE(l.total_cost, 0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS cost_total,
                CASE
                    WHEN SUM(l.qty * u.factor) = 0 THEN NULL
                    ELSE (SUM(COALESCE(l.total_cost, 0) / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) / SUM(l.qty * u.factor))::decimal
                END AS cost_avg,
                MAX(COALESCE(q.qty_available, 0)) AS qty_available
        """
        return select_str

    def _group_by(self):
        group_str = super(PosOrderReport, self)._group_by()
        # No extra GROUP BY needed for aggregated cost fields
        return group_str

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
        """
        return from_str

