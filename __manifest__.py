{
    'name': 'Inspection',
    'version': '17.0.1.0.0',
    'author': 'Tijus Academy',
    'category': 'Tools',
    'summary': 'Displays all activities in a single view',
    'description': 'A module to view all activities across models in one place.',
    'depends': ['base', 'mail'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/activity_view.xml',
        'views/menu_activity.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}