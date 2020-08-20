"""
Template-based email system for Python.
"""
import logging
import os
from typing import Dict
from typing import List

import jinja2
from premailer import Premailer


class DeliveryEngineNotInstalled(Exception):
    """
    This exception is raised when you attempt to use TemplateMail without a delivery engine installed.
    """


class DeliveryNotMade(Exception):
    """
    Called when a delivery cannot be made
    """

    def __init__(self, details, response=None):
        self.details = details
        self.response = response


class MailTemplate:
    def __init__(self, template_dirs: List[str], delivery_engine=None, logger=None):
        """
        :param template_dirs: Directories containing templates.
        """

        _template_dirs = template_dirs
        for path in _template_dirs:
            assert os.path.exists(path)
            assert os.path.isdir(path)

        self.template_environment = jinja2.Environment(
            undefined=jinja2.StrictUndefined,
            loader=jinja2.FileSystemLoader(_template_dirs),
        )

        self.delivery_engine = delivery_engine

        self.logger = logger or logging.getLogger("mailtemplate")

    def _inline_css(self, html_body):
        premailer = Premailer(allow_network=False,)
        return premailer.transform(html_body)

    def render(
        self,
        template_name: str,
        template_layout: str = "basic",
        options: Dict = None,
        *args,
        **kwargs
    ):
        # @todo: validate for theme name
        default_options = {"theme": "light", "inline_css": True}

        final_options = default_options
        if options is not None:
            final_options = {**default_options, **options}

        template_path = os.path.join(
            template_layout, template_name, "content.html.jinja"
        )
        render_template = self.template_environment.get_template(template_path)
        content = render_template.render(*args, **kwargs)
        if final_options["inline_css"]:
            content = self._inline_css(content)

        return content.strip()


__all__ = ["MailTemplate", "DeliveryEngineNotInstalled", "DeliveryNotMade"]
