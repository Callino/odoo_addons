from openerp import models, fields, api
import logging
import xml.etree.ElementTree as ET

_logger = logging.getLogger(__name__)

class remote_phonebook(models.Model):
    _inherit = 'remote.phonebook'

    def _get_type(self):
        types = super(remote_phonebook, self)._get_type()
        types.append(('yealink', 'Yealink'))
        return types

    '''
    <?xml version="1.0" encoding="utf-8"?>
    <XXXIPPhoneDirectory clearlight="true">
    {item_loop}
    <Title>Phonelist</Title>
    <Prompt>Prompt</Prompt>
    <DirectoryEntry>
    <Name>{$NAME}</Name>
    <Telephone>{$PHONE1}</Telephone>
    <Telephone>{$PHONE2}</Telephone>
    </DirectoryEntry>
    {/item_loop}
    </XXXIPPhoneDirectory>
    '''
    def _get_content_yealink(self):
        partners = self._get_partners()
        _logger.debug("got %d partners", len(partners))
        root = ET.Element('RemoteIPPhoneDirectory')
        root.set('clearlight', 'true')
        title = ET.SubElement(root, 'Title')
        title.text = 'Title'
        prompt = ET.SubElement(root, 'Prompt')
        prompt.text = 'Prompt'
        for partner in partners:
            if not (partner.mobile or partner.phone):
                continue
            entry = ET.SubElement(root, 'DirectoryEntry')
            name = ET.SubElement(entry, 'Name')
            name.text = partner.name
            if partner.mobile:
                phone1 = ET.SubElement(entry, 'Telephone')
                phone1.text = partner.mobile
            if partner.phone:
                phone2 = ET.SubElement(entry, 'Telephone')
                phone2.text = partner.phone
        _logger.info("got element %r", root)
        self.content = ET.tostring(root, 'utf-8')

    def _get_content(self):
        if self.type == 'yealink':
            _logger.info("do return content for type yealink")
            return self._get_content_yealink()
        return super(remote_phonebook, self)._get_content()

    type = fields.Selection(selection=_get_type)
    content = fields.Char('Phonebook content', compute=_get_content)
