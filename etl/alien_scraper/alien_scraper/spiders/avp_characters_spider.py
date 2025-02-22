import scrapy
from urllib.parse import urljoin

#TODO: write logic that writes an appropriate planet string to each characters planets array, depending on the values in films array
#TODO: write scraper for xenopedia and integrate its output with avp_characters.json

class AVPCharacterSpider(scrapy.Spider):
    name = 'avp_characters'
    allowed_domains = ['avp.fandom.com']
    start_urls = [
        'https://avp.fandom.com/wiki/Category:Alien_(film)_characters',
        'https://avp.fandom.com/wiki/Category:Aliens_(film)_characters'
    ]

    def parse(self, response):
        category_film = response.url.split('Category:')[1].split('_')[0]

        for character_link in response.css('.category-page__member-link::attr(href)').getall():
            yield scrapy.Request(
                url=urljoin(response.url, character_link),
                callback=self.parse_character,
                meta={'category_film': category_film}
            )

    def parse_character(self, response):
        infobox = response.css('aside.portable-infobox')

        character = {
            'name': infobox.css('figure + h2::text').get().strip() if infobox.css('figure + h2::text').get() else None,
            'rank': infobox.css('div[data-source="rank"] div.pi-data-value::text').get().strip() 
            if infobox.css('div[data-source="rank"] div.pi-data-value::text').get() else None,
            'affiliation': infobox.css('div[data-source="affiliation"] div.pi-data-value a::text').get().strip()
            if infobox.css('div[data-source="affiliation"] div.pi-data-value a::text').get() else None,
            'species': infobox.css('div[data-source="species"] div.pi-data-value a::text').get().strip() if infobox.css('div[data-source="species"] div.pi-data-value a::text').get() else None,
            'height': self.get_infobox_data(infobox, 'height'),
            'hair': self.get_infobox_data(infobox, 'hair'),
            'eyecolor': self.get_infobox_data(infobox, 'eyes'),
            'planets': self.get_list_data(infobox, 'Notable facts', 'planet'),
            'vessels': self.get_list_data(infobox, 'Notable facts', 'vessel'),
            'films': [response.meta['category_film']]
        }

        yield character

    def get_infobox_data(self, infobox, label):
        value = infobox.css(f'div[data-source="{label}"] div.pi-data-value::text').get()
        return value.strip() if value else None

    def get_list_data(self, infobox, label, keyword):
        facts = infobox.css(f'div[data-source="{label.lower()}"] div.pi-data-value::text').get()
        if facts:
            return [item.strip() for item in facts.split(',') if keyword.lower() in item.lower()]
        return []

