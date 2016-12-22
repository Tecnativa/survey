# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import json
from datetime import datetime

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.survey.controllers.main import \
    WebsiteSurvey, dict_soft_update

_logger = logging.getLogger(__name__)


class QuestionDateWebsiteSurvey(WebsiteSurvey):

    # AJAX prefilling of a survey
    @http.route([
        '/survey/prefill/<model("survey.survey"):survey>/<string:token>',
        '/survey/prefill/<model("survey.survey"):survey>/<string:token>/'
        '<model("survey.page"):page>'],
                type='http', auth='public', website=True)
    def prefill(self, survey, token, page=None, **post):
        res = super(QuestionDateWebsiteSurvey, self).prefill(
            survey, token, page, **post)
        res_decoded = json.loads(res.data)

        UserInputLineObj = request.env['survey.user_input_line']
        # Fetch previous answers
        answer_domain = [('user_input_id.token', '=', token)]
        if page:
            answer_domain.append(('page_id', '=', page.id))
        previous_answers = UserInputLineObj.sudo().search(answer_domain)

        # Return non empty answers in a JSON compatible format
        for answer in previous_answers:
            if not answer.skipped:
                answer_tag = '%s_%s_%s' % (
                    answer.survey_id.id,
                    answer.page_id.id,
                    answer.question_id.id)
                answer_value = None
                if answer.answer_type == 'date':
                    date_format = \
                        answer.question_id._get_format_date_lang_context()
                    date = datetime.strptime(
                        answer.value_date_date, "%Y-%m-%d")
                    answer_value = date.strftime(date_format)
                if answer_value:
                    dict_soft_update(res_decoded, answer_tag, answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s "
                        "marked as non skipped" % answer_tag)
        return json.dumps(res_decoded)
