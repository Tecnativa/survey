# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from openerp import api, models
from openerp.tools.translate import _


class Survey(models.Model):
    _inherit = 'survey.survey'

    @api.model
    def prepare_result(self, question, current_filters=None):
        # Calculate and return statistics for date
        if question.type == 'date':
            result = []
            for input_line in question.user_input_line_ids:
                if (not(current_filters) or
                            input_line.user_input_id.id in current_filters):
                    result.append(input_line)
            return result
        else:
            return super(Survey, self).prepare_result(
                question, current_filters)
