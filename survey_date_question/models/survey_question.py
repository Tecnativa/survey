# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from openerp import _, api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    type = fields.Selection(
        selection_add=[('date', _('Date'))],
    )

    def _get_format_date_lang_context(self):
        return self.env['res.lang'].search([
            ('code', '=', self.env.context.get('lang', 'en_US'))
        ]).date_format
    
    @api.model
    def validate_date(self, question, post, answer_tag):
        errors = {}
        answer = post[answer_tag].strip()
        # Empty answer to mandatory question
        if question.constr_mandatory and not answer:
            errors.update({answer_tag: question.constr_error_msg})
        # Checks if user input is a date
        if answer:
            try:
                dateanswer = datetime.datetime.strptime(
                    answer, self._get_format_date_lang_context())
            except ValueError:
                errors.update({answer_tag: _('This is not a date')})
                return errors
        # Answer validation (if properly defined)
        if answer and question.validation_required:
            # Answer is not in the right range
            try:
                dateanswer = datetime.datetime.strptime(answer, DF)
                if not (datetime.datetime.strptime(
                        question.validation_min_date, DF
                        ) <= dateanswer <= datetime.datetime.strptime(
                            question.validation_max_date, DF)):
                    errors.update({answer_tag: question.validation_error_msg})
            except ValueError:
                # check that it is a date has been done hereunder
                pass
        return errors
