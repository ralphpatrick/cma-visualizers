# scrape_panlasang_pinoy.py  (fixed)
import json, time, sys, random
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "https://panlasangpinoy.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Correct category archive URLs:
COURSES = {
    "Breakfast":  "https://panlasangpinoy.com/categories/recipes/breakfast-recipes/",
    "Lunch":      "https://panlasangpinoy.com/categories/recipes/lunch-recipes/",
    "Appetizers": "https://panlasangpinoy.com/categories/recipes/appetizer-recipes/",
    "Dessert":    "https://panlasangpinoy.com/categories/recipes/dessert-and-pastry-recipes/",
    "Dinner":     "https://panlasangpinoy.com/categories/recipes/easy-dinner-recipes/",
}

S = requests.Session()
S.headers.update(HEADERS)

def soup(url):
    for i in range(3):
        try:
            r = S.get(url, timeout=25)
            r.raise_for_status()
            return BeautifulSoup(r.text, "lxml")
        except Exception:
            if i == 2: raise
            time.sleep(1.2 + i * 0.8)

def og_image(post_url):
    try:
        s = soup(post_url)
        m = s.select_one('meta[property="og:image"]')
        if m and m.get("content"):
            v = m["content"].strip()
            return ("https:" + v) if v.startswith("//") else v
    except Exception:
        pass
    return None

def parse_list_page(s, category):
    items = []
    # Grab recipe links from headings and image blocks
    for a in s.select("h2 a[href*='panlasangpinoy.com/'], .entry-content a[href*='panlasangpinoy.com/']"):
        href = (a.get("href") or "").split("#")[0]
        if not href or "/page/" in href:
            continue
        title = (a.get_text(strip=True) or a.get("title") or "").strip()
        # Heuristic: ignore nav/category links
        if not title or title.lower() in {"home","recipes","about","contact"}:
            continue
        items.append({"name": title, "url": href, "img": None, "category": category})
    # de-dupe by URL (some pages list image+title separately)
    uniq, out = set(), []
    for it in items:
        if it["url"] in uniq: 
            continue
        uniq.add(it["url"])
        out.append(it)
    return out

def next_page_url(s):
    # Handles “Next” and numeric pagination
    nxt = s.select_one("a.next, a.next.page-numbers, .page-numbers.current + a.page-numbers")
    if nxt and nxt.get("href"):
        return urljoin(BASE, nxt["href"])
    # Fallback: any anchor with visible text “Next”
    for a in s.select("a"):
        if (a.get_text(strip=True) or "").lower() == "next" and a.get("href"):
            return urljoin(BASE, a["href"])
    return None

def crawl_category(category, start_url):
    results, seen = [], set()
    url, page = start_url, 1
    while url:
        print(f"[{category}] Page {page}: {url}")
        s = soup(url)
        items = parse_list_page(s, category)
        if not items:
            break
        for it in items:
            if it["url"] in seen:
                continue
            seen.add(it["url"])
            img = og_image(it["url"])
            if img:
                it["img"] = img
            results.append(it)
            time.sleep(0.2 + random.random()*0.1)
        url = next_page_url(s)
        page += 1
        time.sleep(0.5 + random.random()*0.2)
    return results

def main():
    all_rows = []
    for cat, url in COURSES.items():
        try:
            rows = crawl_category(cat, url)
            print(f"  -> {cat}: {len(rows)} recipes")
            all_rows.extend(rows)
        except Exception as e:
            print(f"  ! Skipped {cat}: {e}")

    # keep unique by URL
    uniq = {}
    for r in all_rows:
        uniq.setdefault(r["url"], r)

    data = sorted(uniq.values(), key=lambda r: (r["category"], r["name"].lower()))
    with open("pp-dishes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved pp-dishes.json with {len(data)} recipes.")

if __name__ == "__main__":
    sys.exit(main())