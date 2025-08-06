{
    'name': "App",
    'version': '1.0',
    'depends': ['base'],
    'author': "Jaan Nigul",
    'category': '',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_types.xml',
        'views/estate_property_tags.xml',
        'views/estate_menus.xml',
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        
    ],
    'assets': {
        'web.assets_backend': [
            'estate/static/bold_labels.css',
        ],
    }
}