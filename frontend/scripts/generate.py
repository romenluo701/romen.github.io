#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据转换脚本：把 Gmeek.py 的产物（blogBase.json + backup/*.md）转换为
前端 PlanB 数据契约（frontend/data/*.json）并生成 rss.xml。

不修改 Gmeek.py，仅消费其输出，零回归风险。

输入（Gmeek.py 运行后，位于仓库根 APP/romen.github.io/）：
  - blogBase.json    Gmeek 展开的配置快照（含 postListJson / labelColorDict / 站点配置）
  - backup/*.md      每篇文章的 Markdown 原文（文件名 = issue.title 文件名安全化）

输出：
  - frontend/data/config.json
  - frontend/data/postList.json
  - frontend/data/posts/{slug}.json
  - rss.xml（仓库根，后续合并到 docs/）
"""
import argparse
import html
import json
import os
import re
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.dirname(SCRIPT_DIR)          # frontend/
DEFAULT_REPO = os.path.dirname(FRONTEND)        # 仓库根 APP/romen.github.io/
DATA_DIR = os.path.join(FRONTEND, 'data')


def filename_safe(title: str) -> str:
    return re.sub(r'[<>:/\\|?*"]|[\0-\31]', '-', title)


def strip_markdown(text: str) -> str:
    t = re.sub(r'^#{1,6}\s+', '', text.strip())
    t = re.sub(r'[`*_>\[\]()!|]', '', t)
    return t.strip()


def extract_description(markdown: str, fallback: str) -> str:
    if not markdown:
        return fallback
    for line in markdown.splitlines():
        t = strip_markdown(line)
        if t:
            return t
    return fallback


def rfc822(created_at: int) -> str:
    return time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime(created_at))


def build_rss(site, posts, full_posts):
    """手写 RSS 2.0，避免额外依赖。post link 使用新站 URL 格式。"""
    base = site['homeUrl'].rstrip('/')

    def esc(s):
        return html.escape(s, quote=False)

    items = []
    for p in posts:  # posts 已按时间排序
        link = '%s/post/%s/' % (base, p['slug'])
        body = full_posts.get(p['slug'], {}).get('markdown', '')
        desc = extract_description(body, p['description'])
        items.append(
            '<item><title>{t}</title><link>{l}</link><description>{d}</description>'
            '<guid isPermaLink="true">{l}</guid><pubDate>{pd}</pubDate></item>'.format(
                t=esc(p['title']), l=esc(link), d=esc(desc), pd=rfc822(p['createdAtTs']),
            )
        )

    xml = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        '<rss version="2.0">'
        '<channel>'
        '<title>{t}</title><link>{l}</link><description>{d}</description>'
        '<lastBuildDate>{b}</lastBuildDate>'
        '{items}'
        '</channel></rss>'
    ).format(
        t=esc(site['title']),
        l=esc(base + '/'),
        d=esc(site['subTitle']),
        b=rfc822(int(time.time())),
        items=''.join(items),
    )
    return xml


def main():
    parser = argparse.ArgumentParser(description='转换 Gmeek 产物为前端数据')
    parser.add_argument('--repo', default=DEFAULT_REPO,
                        help='blogBase.json 与 backup/ 所在目录（默认仓库根）')
    args = parser.parse_args()

    REPO = os.path.abspath(args.repo)
    BLOGBASE = os.path.join(REPO, 'blogBase.json')
    BACKUP_DIR = os.path.join(REPO, 'backup')

    with open(BLOGBASE, encoding='utf-8') as f:
        blog = json.load(f)

    home_url = blog.get('homeUrl', '')
    # 从 homeUrl 推导 repo：https://user.github.io/repo -> user/repo
    no_proto = home_url.replace('https://', '').replace('http://', '')
    domain, _sep, repo_name = no_proto.partition('/')
    owner = domain.replace('.github.io', '')
    repo = owner + '/' + repo_name if repo_name else owner

    site = {
        'title': blog.get('title', ''),
        'subTitle': blog.get('subTitle', ''),
        'avatarUrl': blog.get('avatarUrl', ''),
        'homeUrl': home_url,
        'repo': repo,
    }

    label_color_dict = blog.get('labelColorDict', {})
    raw_posts = blog.get('postListJson', {})

    full_posts = {}
    posts = []
    os.makedirs(os.path.join(DATA_DIR, 'posts'), exist_ok=True)

    for key in raw_posts:
        if key == 'labelColorDict':
            continue
        p = raw_posts[key]
        # slug 从 postUrl（post/xxx.html）推导
        post_url = p.get('postUrl', '')
        basename = os.path.basename(post_url)
        slug = basename[:-5] if basename.endswith('.html') else basename

        title = p.get('postTitle', '')
        labels = p.get('labels', [])
        created = p.get('createdDate', '')
        created_at = int(p.get('createdAt', 0))
        top = p.get('top', 0)

        # markdown 原文：backup/{safe(title)}.md（复现 Gmeek.py 的命名规则）
        md_path = os.path.join(BACKUP_DIR, filename_safe(title) + '.md')
        markdown = ''
        if os.path.exists(md_path):
            with open(md_path, encoding='utf-8') as f:
                markdown = f.read()

        description = extract_description(markdown, title)

        full_posts[slug] = {
            'slug': slug,
            'title': title,
            'markdown': markdown,
            'labels': labels,
            'createdAt': created,
            'createdAtTs': created_at,
        }
        posts.append({
            'slug': slug,
            'title': title,
            'labels': labels,
            'createdAt': created,
            'description': description,
            'top': top,
            'createdAtTs': created_at,
        })

    # 按时间倒序（新的在前）
    posts.sort(key=lambda x: x['createdAtTs'], reverse=True)

    # 写 data/config.json
    with open(os.path.join(DATA_DIR, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(site, f, ensure_ascii=False, indent=2)

    # 写 data/postList.json（去掉临时字段 createdAtTs）
    plist = {
        'posts': [{k: v for k, v in p.items() if k != 'createdAtTs'} for p in posts],
        'labelColorDict': label_color_dict,
    }
    with open(os.path.join(DATA_DIR, 'postList.json'), 'w', encoding='utf-8') as f:
        json.dump(plist, f, ensure_ascii=False, indent=2)

    # 写 data/posts/{slug}.json（去掉临时字段 createdAtTs）
    for slug, fp in full_posts.items():
        fp_clean = {k: v for k, v in fp.items() if k != 'createdAtTs'}
        with open(os.path.join(DATA_DIR, 'posts', slug + '.json'), 'w', encoding='utf-8') as f:
            json.dump(fp_clean, f, ensure_ascii=False, indent=2)

    # 写 rss.xml
    rss = build_rss(site, posts, full_posts)
    with open(os.path.join(REPO, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write(rss)

    print('生成 %d 篇文章 -> %s' % (len(posts), DATA_DIR))
    print('RSS -> %s' % os.path.join(REPO, 'rss.xml'))


if __name__ == '__main__':
    main()
