from werkzeug.exceptions import NotFound

from odoo import fields, http
from odoo.http import request
from odoo.tools import sql

from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class WebsiteBlogDateUrl(WebsiteBlog):
    @http.route(
        [
            "/blog/<int:year>/<int:month>/<string:slug_str>/",
            "/blog/<int:year>/<int:month>/<string:slug_str>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def blog_post_by_date(self, year, month, slug_str, tag_id=None, page=1, enable_editor=None, **post):
        """Handle WordPress-style date URLs: /blog/YYYY/MM/slug/"""
        BlogPost = request.env["blog.post"]

        blog_post = self._get_post_from_slug(slug_str)
        if not blog_post:
            raise NotFound()

        blog = blog_post.blog_id
        date_begin, date_end = post.get("date_begin"), post.get("date_end")

        domain = request.website.website_domain()
        blogs = blog.search(domain, order="create_date, id asc")

        tag = None
        if tag_id:
            tag = request.env["blog.tag"].browse(int(tag_id))
        blog_url = QueryURL("", ["blog", "tag"], blog=blog, tag=tag, date_begin=date_begin, date_end=date_end)

        tags = request.env["blog.tag"].search([])

        # Find next post
        blog_post_domain = [("blog_id", "=", blog.id)]
        if not request.env.user.has_group("website.group_website_designer"):
            blog_post_domain += [("post_date", "<=", fields.Datetime.now())]

        all_post = BlogPost.search(blog_post_domain)

        if blog_post not in all_post:
            raise NotFound()

        all_post_ids = all_post.ids
        current_blog_post_index = all_post_ids.index(blog_post.id)
        nb_posts = len(all_post_ids)
        next_post_id = all_post_ids[(current_blog_post_index + 1) % nb_posts] if nb_posts > 1 else None
        next_post = next_post_id and BlogPost.browse(next_post_id) or False

        values = {
            "tags": tags,
            "tag": tag,
            "blog": blog,
            "blog_post": blog_post,
            "blogs": blogs,
            "main_object": blog_post,
            "nav_list": self.nav_list(blog),
            "enable_editor": enable_editor,
            "next_post": next_post,
            "date": date_begin,
            "blog_url": blog_url,
        }
        response = request.render("website_blog.blog_post_complete", values)

        if blog_post.id not in request.session.get("posts_viewed", []):
            if sql.increment_fields_skiplock(blog_post, "visits"):
                if not request.session.get("posts_viewed"):
                    request.session["posts_viewed"] = []
                request.session["posts_viewed"].append(blog_post.id)
                request.session.touch()
        return response

    def _get_post_from_slug(self, slug_str):
        """Find a blog.post by matching slug_str against _slugify(post.name)."""
        IrHttp = request.env["ir.http"]
        domain = request.website.website_domain()
        posts = request.env["blog.post"].search(domain)
        for blog_post in posts:
            if IrHttp._slugify(blog_post.name) == slug_str:
                return blog_post
        return None
