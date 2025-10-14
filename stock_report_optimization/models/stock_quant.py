# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Override read_group to optimize performance for large product catalogs.
        This is called by the stock quantity report.
        """
        # Set a reasonable limit if not specified
        if limit is None or limit > 1000:
            limit = 1000
            _logger.info(f"Stock Quant read_group: Limiting results to {limit} for performance")
        
        return super(StockQuant, self).read_group(
            domain, fields, groupby, 
            offset=offset, 
            limit=limit, 
            orderby=orderby, 
            lazy=lazy
        )

    @api.model
    def _read_group_raw(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """
        Override _read_group_raw for additional optimizations
        """
        # Ensure we're not loading too much data at once
        if limit is None or limit > 1000:
            limit = 1000
        
        return super(StockQuant, self)._read_group_raw(
            domain, fields, groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy
        )

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        Override search_read to add automatic limits for performance
        """
        # Limit search results for performance
        if limit is None or limit > 2000:
            limit = 2000
            _logger.info(f"Stock Quant search_read: Limiting results to {limit} for performance")
        
        return super(StockQuant, self).search_read(
            domain=domain,
            fields=fields,
            offset=offset,
            limit=limit,
            order=order
        )

