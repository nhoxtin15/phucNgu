{
    "name": "Support Ticket",
    "version": "1.0",
    "author": "phucnguyen12328",
    "description": """
     Technical Support Ticket module to show available properties
    """,
    "category": "Sales",
    "depends": ['base','web','mail'],
    "data": [
        'security/res_groups.xml',
        'security/ir.model.access.csv',


                  
        'views/ticket_view.xml',

        'views/menu_items.xml',
    ],
    "installable" : True,
    "application" : True,
    "license" : "LGPL-3",
    'auto_install': False,
}