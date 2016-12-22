# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input_line'
    
    @api.multi
    def _answered_or_skipped(self):
        return super(SurveyUserInputLine, self)._answered_or_skipped()
    
    @api.multi
    def _check_answer_type(self):
        res = super(SurveyUserInputLine, self)._check_answer_type()
        for uil in self:
            if uil.answer_type == 'date':
                return bool(uil.value_date_date)
        return res

    value_date_date = fields.Date(string='Value for date fields')
    
    _constraints = [
        (_answered_or_skipped, "A question cannot be unanswered and skipped",
         ['skipped', 'answer_type']),
        (_check_answer_type, "The answer must be in the right type",
         ['answer_type', 'text', 'number', 'date', 'free_text', 'suggestion'])
    ]

    @api.model
    def save_line_date(self, user_input_id, question, post, answer_tag):
        vals = {
            'user_input_id': user_input_id,
            'question_id': question.id,
            'page_id': question.page_id.id,
            'survey_id': question.survey_id.id,
            'skipped': False
        }
        if answer_tag in post and post[answer_tag].strip() != '':
            vals.update({
                'answer_type': 'date',
                'value_date_date': post[answer_tag],
            })
        else:
            vals.update({
                'answer_type': None,
                'skipped': True,
            })
        old_uil = self.search([
            ('user_input_id', '=', user_input_id),
            ('survey_id', '=', question.survey_id.id),
            ('question_id', '=', question.id),
        ])
        if old_uil:
            self.browse(old_uil[0]).write(vals)
        else:
            self.create(vals)
        return True
