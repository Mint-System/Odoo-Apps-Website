# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from lxml import etree

from odoo import models


class Blog(models.Model):
    _inherit = "blog.blog"

    def _get_rss_xml(self, posts, base_url, html2plaintext_func):
        self.ensure_one()

        blog_slug = self.env["ir.http"]._slug(self)
        feed_url = f"{base_url}/blog/{blog_slug}/feed"
        blog_url = f"{base_url}/blog/{blog_slug}"

        NSMAP = {
            "content": "http://purl.org/rss/1.0/modules/content/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "atom": "http://www.w3.org/2005/Atom",
            "sy": "http://purl.org/rss/1.0/modules/syndication/",
        }

        rss = etree.Element("rss", version="2.0", nsmap=NSMAP)

        channel = etree.SubElement(rss, "channel")

        etree.SubElement(channel, "title").text = self.name
        etree.SubElement(channel, "{%s}link" % NSMAP["atom"], href=feed_url, rel="self", type="application/rss+xml")
        link_elem = etree.SubElement(channel, "link")
        link_elem.text = blog_url
        desc_elem = etree.SubElement(channel, "description")
        desc_elem.text = self.subtitle or ""

        if posts:
            last_build_date = posts[0].post_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
            etree.SubElement(channel, "lastBuildDate").text = last_build_date

        etree.SubElement(channel, "language").text = "en-US"
        etree.SubElement(channel, "{%s}updatePeriod" % NSMAP["sy"]).text = "hourly"
        etree.SubElement(channel, "{%s}updateFrequency" % NSMAP["sy"]).text = "1"
        gen_elem = etree.SubElement(channel, "generator")
        gen_elem.text = base_url

        for post in posts:
            self._append_rss_item(channel, post, base_url, html2plaintext_func)

        xml_bytes = etree.tostring(rss, encoding="UTF-8", xml_declaration=False, pretty_print=True)
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes.decode("utf-8")
        return xml_str

    def _make_absolute_urls(self, html, base_url):
        self.ensure_one()
        if not html:
            return html
        pattern = re.compile(r'\b(src|href|data-original-src)\s*=\s*(["\'])(/[^"\']*?)\2', re.IGNORECASE)

        def _replace(match):
            return f"{match.group(1)}={match.group(2)}{base_url}{match.group(3)}{match.group(2)}"

        return pattern.sub(_replace, html)

    def _append_rss_item(self, parent, post, base_url, html2plaintext_func):
        self.ensure_one()
        post_url = f"{base_url}{post.website_url}"

        NSMAP = {
            "content": "http://purl.org/rss/1.0/modules/content/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

        item = etree.SubElement(parent, "item")
        etree.SubElement(item, "title").text = post.name
        link_elem = etree.SubElement(item, "link")
        link_elem.text = post_url
        creator_elem = etree.SubElement(item, "{%s}creator" % NSMAP["dc"])
        creator_elem.text = post.sudo().author_id.name or ""

        if post.post_date:
            pub_date = post.post_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
            etree.SubElement(item, "pubDate").text = pub_date

        for tag in post.tag_ids:
            cat_elem = etree.SubElement(item, "category")
            cat_elem.text = tag.name

        guid = etree.SubElement(item, "guid", isPermaLink="true")
        guid.text = post_url
        desc_elem = etree.SubElement(item, "description")
        desc_elem.text = html2plaintext_func(post.teaser) or ""

        content_elem = etree.SubElement(item, "{%s}encoded" % NSMAP["content"])
        content_elem.text = etree.CDATA(self._make_absolute_urls(post.content or "", base_url))
