# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Survey Date Question',
    'summary': 'Survey Percent Question Type',
    'version': '8.0.0.1.0',
    'author': 'Tecnativa,'
              'Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'license': 'AGPL-3',
    'category': 'Marketing',
    'depends': [
        'survey'
    ],
    'data': [
        'views/survey_result.xml',
        'views/survey_templates.xml',
        # 'views/survey_views.xml',
    ],
    'installable': True,
}
