from openerp import http
import logging


_logger = logging.getLogger(__name__)


class RPBPhonebook(http.Controller):

    @http.route('/rpb/<tokken>', auth='public')
    def index(self, **kw):
        _logger.debug("got %r", kw)
        if 'tokken' not in kw:
            return "Invalid tokken"
        _logger.debug("got %r", kw)
        # Do try to load phonebook with given tokken
        rpb_obj = http.request.env['remote.phonebook']
        _logger.debug("got %r", kw)
        rpb = rpb_obj.sudo().search([('tokken', '=', kw['tokken'])])
        _logger.debug("got %r", rpb)
        if len(rpb) != 1:
            return "Tokken not registered"
        return rpb.content
