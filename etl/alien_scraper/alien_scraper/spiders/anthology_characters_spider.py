import scrapy
from urllib.parse import urljoin

class AnthologyCharactersSpider(scrapy.Spider):
    name = 'anthology_characters_spider'
    allowed_domains = ['alienanthology.fandom.com']

    # Map each category to its canonical film title
    film_titles = {
        'Alien_Resurrection_characters': 'Alien Resurrection',
        'Alien_3_characters': 'Alien 3',
        'Prometheus_characters': 'Prometheus'
    }

    start_urls = [
        'https://alienanthology.fandom.com/wiki/Category:Alien_Resurrection_characters',
        'https://alienanthology.fandom.com/wiki/Category:Alien_3_characters',
        'https://alienanthology.fandom.com/wiki/Category:Prometheus_characters'
    ]

    def parse(self, response):
        """
        Extracts the category from the URL, maps it to a film title,
        and follows links to individual character pages.
        """
        # Get the substring after '/Category:' e.g. 'Alien_3_characters'
        category = response.url.split('/Category:')[1]

        # Look up the corresponding film name
        film_name = self.film_titles.get(category, 'Unknown')

        for character_link in response.css('.category-page__member-link::attr(href)').getall():
            yield scrapy.Request(
                url=urljoin(response.url, character_link),
                callback=self.parse_character,
                meta={'film_name': film_name}
            )

    def parse_character(self, response):
        """
        Parses an individual character page and collects the requested fields.
        """
        infobox = response.css('aside.portable-infobox')

        # Build the character dictionary
        character = {
            'name': response.css('h1.page-header__title span.mw-page-title-main::text').get().strip() \
                    if response.css('h1.page-header__title span.mw-page-title-main::text').get() else None,
            'rank': self.get_rank(infobox),
            'affiliation': self.get_affiliation(infobox),
            'species': self.get_species(infobox),
            'height': self.get_infobox_data(infobox, 'height'),
            'hair': self.get_infobox_data(infobox, 'hair'),
            'eyecolor': self.get_infobox_data(infobox, 'eyes'),
            'planets': [],
            'vessels': [],
            'films': [response.meta['film_name']]
        }

        yield character

    def get_rank(self, infobox):
        """
        Searches for a 'div' with data-source="rank" 
        then retrieves the text from the nested 'div'.
        """
        selector = infobox.css('div[data-source="rank"] div::text').get()
        return selector.strip() if selector else None

    def get_affiliation(self, infobox):
        """
        Searches for a 'div' with data-source="ally" 
        then retrieves the text from an anchor tag inside it.
        """
        selector = infobox.css('div[data-source="ally"] div.pi-data-value a::text').get()
        return selector.strip() if selector else None

    def get_species(self, infobox):
        """
        Searches for a 'div' with data-source="species"
        then retrieves text from an anchor tag inside it.
        """
        selector = infobox.css('div[data-source="species"] div.pi-data-value a::text').get()
        return selector.strip() if selector else None

    def get_infobox_data(self, infobox, label):
        """
        Generic helper to retrieve text from a 'div' 
        in the infobox with `data-source="<label>"`.
        """
        selector = infobox.css(f'div[data-source="{label}"] div.pi-data-value::text').get()
        return selector.strip() if selector else None

