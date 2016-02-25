# __init__.py
# -*- coding: utf-8 -*-
import logging
from openerp import SUPERUSER_ID, api, models, fields
from lxml import etree
from openerp.modules.registry import RegistryManager
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class sol_pa(models.TransientModel):
    _name = 'sol.pa'

    def fields_get(self, cr, uid, fields=None, context=None, write_access=True, attributes=None):
        mf = self.pool.get('ir.model')
        imf = self.pool.get('ir.model.fields')
        model_id = mf.search(cr, uid, [('name','=','sol.pa')])
        res = super(sol_pa, self).fields_get(cr, uid, fields, context, write_access, attributes)
        warehouse_ids = self.pool.get('stock.warehouse').search(cr,SUPERUSER_ID,[])
        for warehouse in self.pool.get('stock.warehouse').browse(cr, SUPERUSER_ID, warehouse_ids):
            field_name = 'x_warehouse_qty_%d' % warehouse.id
            vfield_name = 'x_warehouse_vqty_%d' % warehouse.id
            if not field_name in res:
                new_field = {
                    'name': field_name,
                    'field_description': _('Available %s') % warehouse.code,
                    'ttype': 'float',
                    'model_id': model_id[0],
                    'state': 'manual',
                }
                _logger.debug("do create field: %r", new_field)
                imf.create(cr, uid, new_field)
                new_field = {
                    'name': vfield_name,
                    'field_description': _('Virtual %s') % warehouse.code,
                    'ttype': 'float',
                    'model_id': model_id[0],
                    'state': 'manual',
                }
                _logger.debug("do create field: %r", new_field)
                imf.create(cr, uid, new_field)
        for field in res:
            if field.startswith('x_warehouse_qty_'):
                wid = field.replace("x_warehouse_qty_","")
                wid = int(wid)
                if wid not in warehouse_ids:
                    column_id = imf.search(cr, uid, [('name', '=', field),('model_id', '=', model_id[0])], limit=1)
                    _logger.debug("we do have to delete column %r", column_id)
                    imf.unlink(cr, uid, column_id[0])
            if field.startswith('x_warehouse_vqty_'):
                wid = field.replace("x_warehouse_vqty_","")
                wid = int(wid)
                if wid not in warehouse_ids:
                    column_id = imf.search(cr, uid, [('name', '=', field),('model_id', '=', model_id[0])], limit=1)
                    _logger.debug("we do have to delete column %r", column_id)
                    imf.unlink(cr, uid, column_id[0])
        return res

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        self._get_default_tree_view(cr, uid, context)
        res = super(sol_pa,self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        return res

    def _get_default_tree_view(self, cr, uid, context):
        self.fields_get(cr, uid)
        _logger.debug("get default tree view got called")
        root = etree.Element("tree", string="Produkt Verfuegbarkeit")
        etree.SubElement(root, 'field', name='product_id')
        etree.SubElement(root, 'field', name='qty')
        warehouse_ids = self.pool.get('stock.warehouse').search(cr,SUPERUSER_ID,[])
        for warehouse in self.pool.get('stock.warehouse').browse(cr, SUPERUSER_ID, warehouse_ids):
            etree.SubElement(root, 'field', name='x_warehouse_qty_%d' % warehouse.id)
            etree.SubElement(root, 'field', name='x_warehouse_vqty_%d' % warehouse.id)
        _logger.debug("xml: %s", etree.tostring(root))
        return root

    order_id = fields.Many2one('sale.order', 'Bestellung')
    product_id = fields.Many2one('product.product', 'Produkt')
    qty = fields.Float('Bestellt')


class sale_order(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.v8
    def compute_sol_pa(self):
        for sale in self:
            sale.sol_pa_lines = []
            sol_pa_obj = self.env['sol.pa']
            warehouse_obj = self.env['stock.warehouse']
            warehouse_ids = warehouse_obj.search([])
            for sol in sale.order_line:
                pa = sol_pa_obj.search([('order_id', '=', sol.order_id.id),('product_id','=',sol.product_id.id)], limit=1)
                pa_data = {}
                for warehouse_id in warehouse_ids:
                    pa_data['x_warehouse_vqty_%d'%warehouse_id.id] = sol.with_context(warehouse=warehouse_id.id).product_id.virtual_available
                    pa_data['x_warehouse_qty_%d'%warehouse_id.id] = sol.with_context(warehouse=warehouse_id.id).product_id.qty_available
                if pa:
                    pa_data.update({
                        'qty': sol.product_uom_qty,
                    })
                    pa.write(pa_data)
                    sale.sol_pa_lines += pa
                else:
                    pa_data.update({
                        'order_id': sol.order_id.id,
                        'product_id': sol.product_id.id,
                        'qty': sol.product_uom_qty,
                    })
                    pa = sol_pa_obj.create(pa_data)
                    sale.sol_pa_lines += pa

    sol_pa_lines = fields.One2many(comodel_name='sol.pa', inverse_name='order_id', string='Product Availability', compute=compute_sol_pa)
