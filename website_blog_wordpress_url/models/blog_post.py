# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class BlogPost(models.Model):
    _inherit = "blog.post"

    def _compute_website_url(self):
        super()._compute_website_url()
        for blog_post in self:
            if blog_post.id:
                date = blog_post.post_date or blog_post.create_date
                if date:
                    year = date.strftime("%Y")
                    month = date.strftime("%m")
                    slug = self.env["ir.http"]._slugify(blog_post.name)
                    blog_post.website_url = "/blog/%s/%s/%s/" % (year, month, slug)
