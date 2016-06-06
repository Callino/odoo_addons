from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class remote_phonebook(models.Model):
    _name = 'remote.phonebook'

    def _get_type(self):
        return [('csv', 'CSV')]

    def _get_partners(self):
        return self.env['res.partner'].search([('user_id', '=', self.user_id.id)])

    def _get_content_csv(self):
        partners = self._get_partners()
        _logger.debug("got %d partners", len(partners))
        csv = ""
        for partner in partners:
            csv = csv + partner.name + "\r\n"
        self.content = csv

    def _get_content(self):
        if self.type == 'csv':
            return self._get_content_csv()
        return ''

    def _get_url(self):
        self.url = self.env['ir.config_parameter'].get_param('web.base.url') + "/rpb/" + self.tokken

    name = fields.Char('Phonebook')
    tokken = fields.Char('Access Tokken')
    type = fields.Selection(selection=_get_type)
    description = fields.Text('Description')
    url = fields.Char('Access URL', compute=_get_url)
    user_id = fields.Many2one(comodel_name='res.users', string='Benutzer')
    content = fields.Char('Phonebook content', compute=_get_content)
