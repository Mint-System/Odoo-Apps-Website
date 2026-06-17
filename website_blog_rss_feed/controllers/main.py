from odoo import fields, http
from odoo.http import request
from odoo.tools import html2plaintext

from odoo.addons.website_blog.controllers.main import WebsiteBlog as WebsiteBlogOriginal


class WebsiteBlog(WebsiteBlogOriginal):
    @http.route(
        ["/blog/feed", '/blog/<model("blog.blog"):blog>/feed'], type="http", auth="public", website=True, sitemap=True
    )
    def blog_feed(self, blog=None, limit="15", **kwargs):
        if not blog:
            blog = request.env["blog.blog"].sudo().search([], limit=1, order="id ASC")
            if not blog:
                return request.not_found()
        return self._blog_feed_xml(blog, limit, **kwargs)

    def _blog_feed_xml(self, blog, limit="15", **kwargs):
        blog.ensure_one()
        domain = [
            ("blog_id", "=", blog.id),
            ("website_published", "=", True),
            ("post_date", "<=", fields.Datetime.now()),
        ]
        posts = request.env["blog.post"].search(domain, limit=min(int(limit), 50), order="post_date DESC")
        base_url = blog.get_base_url()
        xml = blog._get_rss_xml(posts, base_url, html2plaintext)
        return request.make_response(xml, headers=[("Content-Type", "application/rss+xml")])
