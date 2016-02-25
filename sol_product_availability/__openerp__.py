# __openerp__.py
{
    "name" : "SOL Product Availabilty",
    "version" : "1.0",
    "author" : "Callino (Wolfgang Pichler)",
    "category" : "Sales Management",
    "website" : "http://www.callino.at/",
    'summary': "Product availability in sale order lines",
    'description': """
Product Availabilty in Sale Order Lines
==========================================

This Module will add a new tab Availabilty to sale orders<br/>
You will search for each sale order line the product availability for each warehouse

    """,
    'depends': ['base', 'crm', 'sale', 'stock'],
    "update_xml" : ["sol_product_availabilty.xml"],
    "installable": True,
    "auto_install": False,
    "active": False
}