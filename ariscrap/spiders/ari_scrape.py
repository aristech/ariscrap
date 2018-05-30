import scrapy
from ariscrap.items import AriItem
from datetime import datetime
import re

# scrapy crawl ari_scraper -o files/file_name.csv

class Aris(scrapy.Spider):
    name = "ari_scraper"

    # First Start Url (if you want you can use query url as start url)
    start_urls = ["https://#"]

    # Usually the same as start_urls
    page_urls = "https://#"


    custom_settings = {
        # specifies exported fields and order. It should match the fields in /items.py
        'FEED_EXPORT_FIELDS': ["companyTitle", "status", "client", "supplier", "companystreetAddress", "companypostalCode", "companyaddressLocality", "companyaddressRegion", "companyPhone", "companysite", "companyEmail", "companysubTitle", "category", "sales_rep", "companyShortDescription", "companyLongDescription" ,"img"],
    }

    npages = 2

    # This mimics getting the pages using the next button.
    for i in range(2, npages + 1):
        start_urls.append(
            # Change accordingly
            page_urls + "&page=" + str(i) + "")

    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'listingBusinessNameArea')]//h2//a[contains(@class, 'et-v2')]//@href"):

            # Starting point for pagination. Usually the domain name. Add the scheme, eg http://
            url = "https://#" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = AriItem()

        #extra fields for manual insertion in the csv
        category  = 'Restaurants'
        sales_rep = 'Penny'

        # Getting Company Title
        item['companyTitle'] = "".join(response.xpath(
            "//span[contains(@id, 'ProfileLabel')]/descendant::text()").extract()[0].strip())


        # Getting Company company subTitle
        item['companysubTitle'] = "".join(response.xpath(
            "//span[@id='ProfileSubLabel']/descendant::text()").extract()[0].strip())


        # Getting company street Address
        item['companystreetAddress'] = " ".join(response.xpath(
            "//a[contains(@class, 'xoevn et-v2')]//span[1]/text()").extract())


        # Getting company street Address
        item['companystreetAddress'] = " ".join(response.xpath(
            "//a[contains(@class, 'xoevn et-v2')]//span[1]/text()").extract())


        # Getting company postalC ode
        item['companypostalCode'] = " ".join(response.xpath(
            "//a[contains(@class, 'xoevn et-v2')]//span[@itemprop='postalCode']/text()").extract())


        # Getting company address Locality
        item['companyaddressLocality'] = " ".join(response.xpath(
            "//a[contains(@class, 'xoevn et-v2')]//span[@itemprop='addressLocality']/text()").extract())


        # Getting company address Region
        item['companyaddressRegion'] = " ".join(response.xpath(
            "//a[contains(@class, 'xoevn et-v2')]//span[@itemprop='addressRegion']/text()").extract())


        # Getting company Phone
        item['companyPhone'] = " ".join(response.xpath(
            "//span[contains(@itemprop, 'telephone')]//a[contains(@class, 'xoevn et-v2')]/text()").extract())

        # Getting company Website
        item['companysite'] = " ".join(response.xpath(
            "//span[contains(@itemprop, 'url')]/@content").extract())

        # Getting company email
        item['companyEmail'] = " ".join(response.xpath(
            "//span[contains(@itemprop, 'email')]/@content").extract())

        # Getting Short Story
        item['companyShortDescription'] = " ".join(response.xpath(
            "//section[contains(@id, 'shortProfile')]//h3/descendant::text()").extract())

        # Getting Story
        story_list = response.xpath(
            "//div[contains(@id, 'text-of-short-profile')]//p/descendant::text()").extract()
        story_list = [x.strip() for x in story_list if len(x.strip()) > 0]
        item['companyLongDescription'] = " ".join(story_list)

        # CRMclient status (0 (closed) or 1 (active)) \\\ custom field ///
        item['status'] = "1"

        # CRMclient status (0 (no customer no prospect)/1 (customer)/2 (prospect)/3 (customer and prospect)) \\\ custom field ///
        item['client'] = "2"

        # supplier status (0 or 1) \\\ custom field ///
        item['supplier'] = "0"

        # Url (The link to the page) \\\ custom field for generic image ///
        item['img'] = category +"10.png"

        # Representative \\\ custom field ///
        item['sales_rep'] = sales_rep

        # Category  \\\ custom field ///
        item['category'] = category

        yield item
