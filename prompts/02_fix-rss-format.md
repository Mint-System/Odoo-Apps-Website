---
title: "Fix RSS format"
state: completed
model: infomaniak/moonshotai/Kimi-K2.6
input_tokens: "28.0K"
---

# Run 02

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

@Clanker Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I need you to update `website_blog_rss_feed` module. There are two issues.

The first issue is the xml header of the resulting rss file. It starts with
`<?xml version='1.0' encoding='UTF-8'?>` but it should be
`<?xml version="1.0" encoding="UTF-8"?>`.

So double quotes instead of single quotes.

Then the second issue is about urls in the posts. A post may contain images like this:

```
<p><img src="/web/image/33994-46aaf0dd/HillShading.webp?access_token=c7239dc3-6139-4b0a-af67-02a78fb00963" alt="" class="img img-fluid o_we_custom_image" data-mimetype="image/webp" data-original-id="33988" data-original-src="/web/image/33988-1b0c9f0d/HillShading.png" data-mimetype-before-conversion="image/png" data-resize-width="NaN" loading="lazy"></p>
```

The source url is relative and must be absolute. Make sure that relative paths like
`/web/image` are replaces with absolute path `{domain}/web/image`.

The domain is taken from `website` and if it is not set fall back to the Odoo system
param `web.base.url`.

## Worklog

Fixed two issues in `addons/website/website_blog_rss_feed/models/blog.py`:

1. **XML declaration quotes:** Changed `etree.tostring(..., xml_declaration=True)` to
   `xml_declaration=False` and manually prepended
   `<?xml version="1.0" encoding="UTF-8"?>`, ensuring double quotes instead of single
   quotes.
2. **Relative to absolute URLs:** Added `_make_absolute_urls` helper method that uses a
   regex to find `src`, `href`, and `data-original-src` attributes with relative paths
   (starting with `/`) and prepends the `base_url` (which already resolves website
   domain → `web.base.url`). The encoded RSS item content now passes through this helper
   before being wrapped in CDATA.

Syntax check passed with `python -m py_compile`.
