import os
import json
from random import random
from time import sleep
import scrapy.http as sh
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional, TypedDict
"""
{
  "id": "5tfHfwnhyyM",
  "slug": "man-in-black-crew-neck-shirt-5tfHfwnhyyM",
  "alternative_slugs": {
    "en": "man-in-black-crew-neck-shirt-5tfHfwnhyyM",
    "es": "hombre-con-camisa-negra-de-cuello-redondo-5tfHfwnhyyM",
    "ja": "黒のクルーネックシャツを着た男-5tfHfwnhyyM",
    "fr": "homme-en-chemise-noire-a-col-rond-5tfHfwnhyyM",
    "it": "uomo-in-camicia-girocollo-nera-5tfHfwnhyyM",
    "ko": "맨-인-블랙-크루넥-셔츠-5tfHfwnhyyM",
    "de": "mann-in-schwarzem-rundhalsshirt-5tfHfwnhyyM",
    "pt": "homem-na-camisa-preta-do-pescoco-da-tripulacao-5tfHfwnhyyM"
  },
  "created_at": "2020-07-21T16:08:46Z",
  "updated_at": "2024-11-05T23:49:29Z",
  "promoted_at": null,
  "width": 2624,
  "height": 3936,
  "color": "#260c0c",
  "blur_hash": "L66HGvtR0#xv?HtRJBxu5Sxu~Bt7",
  "description": null,
  "alt_description": "man in black crew neck shirt",
  "breadcrumbs": [],
  "urls": {
    "raw": "https://images.unsplash.com/photo-1595347097560-69238724e7bd?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg&ixlib=rb-4.0.3",
    "full": "https://images.unsplash.com/photo-1595347097560-69238724e7bd?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg&ixlib=rb-4.0.3&q=85",
    "regular": "https://images.unsplash.com/photo-1595347097560-69238724e7bd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg&ixlib=rb-4.0.3&q=80&w=1080",
    "small": "https://images.unsplash.com/photo-1595347097560-69238724e7bd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg&ixlib=rb-4.0.3&q=80&w=400",
    "thumb": "https://images.unsplash.com/photo-1595347097560-69238724e7bd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg&ixlib=rb-4.0.3&q=80&w=200",
    "small_s3": "https://s3.us-west-2.amazonaws.com/images.unsplash.com/small/photo-1595347097560-69238724e7bd"
  },
  "links": {
    "self": "https://api.unsplash.com/photos/man-in-black-crew-neck-shirt-5tfHfwnhyyM",
    "html": "https://unsplash.com/photos/man-in-black-crew-neck-shirt-5tfHfwnhyyM",
    "download": "https://unsplash.com/photos/5tfHfwnhyyM/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg",
    "download_location": "https://api.unsplash.com/photos/5tfHfwnhyyM/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MjF8fG1hbnxlbnwwfHx8fDE3MzI2MzYzNDV8Mg"
  },
  "likes": 142,
  "liked_by_user": false,
  "current_user_collections": [],
  "sponsorship": null,
  "topic_submissions": {},
  "asset_type": "photo",
  "premium": false,
  "plus": false,
  "user": {
    "id": "3lESrGTOryA",
    "updated_at": "2024-11-20T22:58:53Z",
    "username": "bentofan",
    "name": "Ben Tofan",
    "first_name": "Ben",
    "last_name": "Tofan",
    "twitter_username": null,
    "portfolio_url": "https://bentofan.au",
    "bio": "Creative Designer / Photographer",
    "location": "Sydney, Australia",
    "links": {
      "self": "https://api.unsplash.com/users/bentofan",
      "html": "https://unsplash.com/@bentofan",
      "photos": "https://api.unsplash.com/users/bentofan/photos",
      "likes": "https://api.unsplash.com/users/bentofan/likes",
      "portfolio": "https://api.unsplash.com/users/bentofan/portfolio",
      "following": "https://api.unsplash.com/users/bentofan/following",
      "followers": "https://api.unsplash.com/users/bentofan/followers"
    },
    "profile_image": {
      "small": "https://images.unsplash.com/profile-1705632733544-b9e869f63a11image?ixlib=rb-4.0.3&crop=faces&fit=crop&w=32&h=32",
      "medium": "https://images.unsplash.com/profile-1705632733544-b9e869f63a11image?ixlib=rb-4.0.3&crop=faces&fit=crop&w=64&h=64",
      "large": "https://images.unsplash.com/profile-1705632733544-b9e869f63a11image?ixlib=rb-4.0.3&crop=faces&fit=crop&w=128&h=128"
    },
    "instagram_username": "bentofan.au",
    "total_collections": 0,
    "total_likes": 16,
    "total_photos": 156,
    "total_promoted_photos": 15,
    "total_illustrations": 0,
    "total_promoted_illustrations": 0,
    "accepted_tos": true,
    "for_hire": true,
    "social": {
      "instagram_username": "bentofan.au",
      "portfolio_url": "https://bentofan.au",
      "twitter_username": null,
      "paypal_email": null
    }
  },
  "tags_preview": [
    {
      "type": "search",
      "title": "man"
    },
    {
      "type": "search",
      "title": "sydney nsw"
    },
    {
      "type": "search",
      "title": "australia"
    }
  ],
  "search_source": "keyword"
}
"""
class UnsplashSpider(scrapy.Spider):
    class SearchResponse(TypedDict):
        class SearchResponseResult(TypedDict):
            class Url(TypedDict):
                raw: str
                full: str
            id: str
            slug: str
            urls: Url
            description: Optional[str]
            alt_description: str
        total: int
        total_pages: int
        results: list[SearchResponseResult]
    name = 'unsplash_spider'
    allowed_domains = ['unsplash.com']
    root_dir = "output"  # Customize your root directory
    state_file = "resume.json"
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Base delay
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Default behavior for randomization
        'COOKIES_ENABLED': False,
    }
    cookies: dict[str, dict[str,str]] = dict()
    responses: dict[str, sh.Response] = dict()
    pages: dict[str, int] = dict()
    process_queue: dict[str,tuple[str,str,str]] = dict()
    processed_ids: set[str] = set()
    def __init__(self, tags: str, per_page=100, max_count_per_tag=5000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = tags.split(',')
        self.per_page = per_page
        self.max_count_per_tag = max_count_per_tag
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
    def start_requests(self):
        self.load_state()
        for id, meta in self.process_queue.items():
            yield self.process_queued(id, meta)
        for tag in self.tags:
            meta = { 'tag': tag }
            url = f'https://unsplash.com/s/photos/{tag}?license=free'
            yield sh.Request(url, callback=self.parse_tag_page, meta=meta)
    def get_cookies(self, tag: str, url: str):
        self.driver.get(url)
        sleep(5+2.5*random())
        cookies = self.driver.get_cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies if cookie['path']=='/'}
        cookies_dict.update({
            'xp-search-region-awareness': 'experiment',
            'xp-enable-embedded-checkout': 'control'
        })
        self.cookies[tag] = cookies_dict
    def parse_tag_page(self, response: sh.Response):
        tag = response.meta['tag']
        self.responses[tag] = response
        self.get_cookies(tag, response.url)
        meta = { 'tag': tag }
        page = self.pages.get(tag, 1)
        url = f'https://unsplash.com/napi/search/photos?page={page}&per_page={self.per_page}&plus=none&query={tag}&xp=search-region-awareness%3Aexperiment'
        yield response.follow(url, method='GET', cookies=self.cookies[tag], callback=self.parse_page_list, meta=meta)
    def process_queued(self, id: str, meta: tuple[str, str, str]):
        tag, desc, url = meta
        meta = { 'id': id, 'description': desc, 'tag': tag }
        return sh.Request(url, self.save_img, meta=meta)
    def parse_page_list(self, response: sh.TextResponse):
        res_obj: UnsplashSpider.SearchResponse = response.json()

        tag = response.meta['tag']
        count = response.meta.get('count', 0)
        page = self.pages.get(tag, 1)  # Track the current page number (starting at 0)

        photos = res_obj['results']
        if (len(photos) <= 0):
            return
        # Process emoji items
        for photo in photos:
            id = photo['id']
            if not id in self.processed_ids: 
                dl_url = photo['urls']['raw']
                description = photo['description'] if photo['description'] else photo['alt_description']
                meta = (tag, description, dl_url)
                self.process_queue[id] = meta
                yield self.process_queued(id, meta)
                count += 1
                if count >= self.max_count_per_tag:
                    return  # Stop if we've processed the max count
        # If not, proceed to the next page
        if page >= res_obj['total_pages']:
            return
        page = page + 1
        self.pages[tag] = page
        next_page_url = f"{response.url.split('?')[0]}?page={page}&per_page={self.per_page}&plus=none&query={tag}&xp=search-region-awareness%3Aexperiment"
        meta = { 'tag': tag, 'count': count, 'page': page }
        yield self.responses[tag].follow(next_page_url, method='GET', cookies=self.cookies[tag], callback=self.parse_page_list, meta=meta)
    def closed(self, reason):
        """Saves the state when the spider is closed."""
        self.save_state()
        self.log(f"Spider closed: {reason}")
    def load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                saved_state = json.load(f)
                self.pages = saved_state.get('pages', {})
                self.process_queue = saved_state.get('process_queue',{})
                self.processed_ids = set(saved_state.get('processed_links', []))
        except FileNotFoundError:
            pass
    def save_state(self):
        state = {
            "pages": self.pages,
            "process_queue": self.process_queue,
            "processed_links": list(self.processed_ids),
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
    def save_img(self, response: sh.Response):
        content_type = response.headers.get('Content-Type').decode('utf-8')
        image_type = content_type.split('/')[1]

        id = response.meta['id']
        tag = response.meta['tag']
        desc = response.meta['description']

        category_dir = os.path.join(self.root_dir, tag)
        os.makedirs(category_dir, exist_ok=True)

        # Construct the full file path
        img_path = os.path.join(category_dir, f'{id}.{image_type}')
        caption_path = os.path.join(category_dir, f'{id}.txt')

        # Save the image to the file system
        with open(img_path, 'wb') as f:
            f.write(response.body)
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(desc)

        self.processed_ids.add(id)
        self.process_queue.pop(id, None)
        self.log(f"Downloaded {id} to {img_path}")
