---
title: "Implement RSS feed feature"
state: draft
---

# Run 01

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

@Clanker when working on this task, make sure to:

- Read context and task section first
- Prepare a list of todos
- Update the todo list while working on the task

## Context

Read the `AGENTS.md` and `README.md` to get an understanding of the project.

## Task

I want you to implement the `website_blog_rss_feed` module. To goal is to recreate the
Wordpress RSS feed feature for Odoo.

Here is an example feed (the content has been striped) of <https://ocad.com/blog/feed/>:

```
<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	>

<channel>
	<title>OCAD Blog</title>
	<atom:link href="https://ocad.com/blog/feed/" rel="self" type="application/rss+xml" />
	<link>https://ocad.com/blog</link>
	<description>OCAD the Smart Software for Cartography</description>
	<lastBuildDate>Thu, 04 Jun 2026 08:30:41 +0000</lastBuildDate>
	<language>en-US</language>
	<sy:updatePeriod>
	hourly	</sy:updatePeriod>
	<sy:updateFrequency>
	1	</sy:updateFrequency>
	<generator>https://wordpress.org/?v=6.8.5</generator>
	<item>
		<title>How OCAD Helps you With Positioning and Mapping in the Field</title>
		<link>https://ocad.com/blog/2026/06/how-ocad-helps-you-with-positioning-and-mapping-in-the-field/</link>
					<comments>https://ocad.com/blog/2026/06/how-ocad-helps-you-with-positioning-and-mapping-in-the-field/#respond</comments>

		<dc:creator><![CDATA[OCAD Team]]></dc:creator>
		<pubDate>Thu, 04 Jun 2026 08:28:21 +0000</pubDate>
				<category><![CDATA[OCAD 11]]></category>
		<category><![CDATA[OCAD 12]]></category>
		<category><![CDATA[OCAD 2018]]></category>
		<category><![CDATA[Uncategorized]]></category>
		<category><![CDATA[Background Maps]]></category>
		<category><![CDATA[LiDAR]]></category>
		<category><![CDATA[OCAD App]]></category>
		<category><![CDATA[Online Map Services]]></category>
		<category><![CDATA[Orienteering]]></category>
		<category><![CDATA[Orienteering Map Making]]></category>
		<category><![CDATA[Professional Map Making]]></category>
		<category><![CDATA[Real Time GPS]]></category>
		<guid isPermaLink="false">https://ocad.com/blog/?p=2353</guid>

					<description><![CDATA[In this blog post, we’ll show you the tools OCAD offers for adding great base data to your mapping project—tools that help you determine your location in the field and allow you to identify and map terrain features, vegetation, and man-made objects. As you’ll see at the end of this article, all of this base [&#8230;]]]></description>
										<content:encoded><![CDATA[]]></content:encoded>

					<wfw:commentRss>https://ocad.com/blog/2026/06/how-ocad-helps-you-with-positioning-and-mapping-in-the-field/feed/</wfw:commentRss>
			<slash:comments>0</slash:comments>


			</item>
		<item>
		<title>New Functions Added to OCAD App</title>
		<link>https://ocad.com/blog/2026/04/new-functions-added-to-ocad-app/</link>
					<comments>https://ocad.com/blog/2026/04/new-functions-added-to-ocad-app/#respond</comments>

		<dc:creator><![CDATA[OCAD Team]]></dc:creator>
		<pubDate>Mon, 27 Apr 2026 21:17:04 +0000</pubDate>
				<category><![CDATA[OCAD 11]]></category>
		<category><![CDATA[OCAD 12]]></category>
		<category><![CDATA[OCAD 2018]]></category>
		<category><![CDATA[Uncategorized]]></category>
		<category><![CDATA[Mobile Mapping]]></category>
		<category><![CDATA[OCAD App]]></category>
		<category><![CDATA[Orienteering Map Making]]></category>
		<guid isPermaLink="false">https://ocad.com/blog/?p=2439</guid>

					<description><![CDATA[]]></description>
										<content:encoded><![CDATA[]]></content:encoded>

					<wfw:commentRss>https://ocad.com/blog/2026/04/new-functions-added-to-ocad-app/feed/</wfw:commentRss>
			<slash:comments>0</slash:comments>


			</item>
		<item>
		<title>GPS in Orienteering Map Making</title>
		<link>https://ocad.com/blog/2026/04/gps-in-orienteering-map-making/</link>
					<comments>https://ocad.com/blog/2026/04/gps-in-orienteering-map-making/#respond</comments>

		<dc:creator><![CDATA[OCAD Team]]></dc:creator>
		<pubDate>Wed, 15 Apr 2026 13:39:18 +0000</pubDate>
				<category><![CDATA[OCAD 11]]></category>
		<category><![CDATA[OCAD 12]]></category>
		<category><![CDATA[OCAD 2018]]></category>
		<category><![CDATA[Uncategorized]]></category>
		<category><![CDATA[Mobile Mapping]]></category>
		<category><![CDATA[OCAD App]]></category>
		<category><![CDATA[Orienteering Map Making]]></category>
		<category><![CDATA[Real Time GPS]]></category>
		<guid isPermaLink="false">https://ocad.com/blog/?p=2240</guid>

					<description><![CDATA[GPS helps you to determine your position in the terrain when mapping, especially when the base data isn’t very accurate. But how exactly does GPS work, and what should you bear in mind when using it? On the website GPS in Orienteering Map Map Making, you&#8217;ll find a summary of useful information about GPS and [&#8230;]]]></description>
										<content:encoded><![CDATA[]]></content:encoded>

					<wfw:commentRss>https://ocad.com/blog/2026/04/gps-in-orienteering-map-making/feed/</wfw:commentRss>
			<slash:comments>0</slash:comments>


			</item>
		<item>
		<title>Webinar: Introduction to the new OCAD App</title>
		<link>https://ocad.com/blog/2026/03/webinar-introduction-to-the-new-ocad-app/</link>
					<comments>https://ocad.com/blog/2026/03/webinar-introduction-to-the-new-ocad-app/#comments</comments>

		<dc:creator><![CDATA[OCAD Team]]></dc:creator>
		<pubDate>Wed, 04 Mar 2026 14:55:36 +0000</pubDate>
				<category><![CDATA[OCAD 11]]></category>
		<category><![CDATA[OCAD 12]]></category>
		<category><![CDATA[OCAD 2018]]></category>
		<category><![CDATA[Uncategorized]]></category>
		<category><![CDATA[Course Setting]]></category>
		<category><![CDATA[Orienteering]]></category>
		<category><![CDATA[Orienteering Map Making]]></category>
		<guid isPermaLink="false">https://ocad.com/blog/?p=2402</guid>

					<description><![CDATA[We are hosting a webinar to introduce you to our new OCAD App and explain step by step how you can use it. Date: Wednesday, 11.03.2026 Time: 19.00-20:30 (UTC+01:00) Amsterdam, Berlin, Bern, Rom, Stockholm, Wien Take the opportunity and ask us questions about the app directly during the webinar. Register here! We look forward to [&#8230;]]]></description>
										<content:encoded><![CDATA[]]></content:encoded>

					<wfw:commentRss>https://ocad.com/blog/2026/03/webinar-introduction-to-the-new-ocad-app/feed/</wfw:commentRss>
			<slash:comments>4</slash:comments>


			</item>
	</channel>
</rss>
```

The `channel` relates to `blog.blog` and `item` to `blog.post`.

I have created all the necessary files to implement the feature:

- `website_blog_rss_feed/controllers/main.py`: Create a route for `/blog/feed` that
  returns the feed for the first blog and another route
  `/blog/<blog.slug>-<blog.id>/feed` that returns the feed of selected blog.
- `website_blog_rss_feed/models/blog_post.py`: If you need some logic to prepare the RSS
  data.
- `website_blog_rss_feed/views/website_blog_templates.xml`: Setup the RSS feed templates
  in there.

Odoo does support an atom feed. I want you to overwrite the functionality and routes.

When implementing not that:

- Comments are not supported
- Categories are `blog.tag`
- Permalink is `website_url`
- lastBuildDate is the date of the last blog post
- The RSS feed is always built dynamically
- generator is `https://odoo.com`

When adding helper function, add them to `blog.blog`.

Ask if something is not unclear.

## Worklog

@Clanker Add a summary here once the task has been completed.

@Clanker Set frontmatter state to completed.
