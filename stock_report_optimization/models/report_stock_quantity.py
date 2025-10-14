# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import logging

_logger = logging.getLogger(__name__)


class ReportStockQuantity(models.Model):
    _inherit = 'report.stock.quantity'

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Optimize read_group for stock quantity report with large datasets
        """
        # Apply reasonable limits
        if limit is None or limit > 500:
            limit = 500
            _logger.info(f"Report Stock Quantity: Limiting to {limit} records for performance")
        
        # Add filter to exclude zero quantities by default if not explicitly requested
        has_quantity_filter = any('quantity' in str(d) for d in domain if d)
        if not has_quantity_filter:
            domain = domain + [('quantity', '!=', 0)]
            _logger.info("Report Stock Quantity: Added filter to exclude zero quantities")
        
        return super(ReportStockQuantity, self).read_group(
            domain, fields, groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy
        )

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Override _read_group_raw with optimizations
        """
        if limit is None or limit > 500:
            limit = 500
        
        return super(ReportStockQuantity, self)._read_group_raw(
            domain, fields, groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy
        )

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        Optimize search_read for stock quantity report
        """
        if limit is None or limit > 1000:
            limit = 1000
            _logger.info(f"Report Stock Quantity search_read: Limiting to {limit}")
        
        # Filter out zero quantities by default
        if domain is None:
            domain = []
        
        has_quantity_filter = any('quantity' in str(d) for d in domain if d)
        if not has_quantity_filter:
            domain = domain + [('quantity', '!=', 0)]
        
        return super(ReportStockQuantity, self).search_read(
            domain=domain,
            fields=fields,
            offset=offset,
            limit=limit,
            order=order
        )

