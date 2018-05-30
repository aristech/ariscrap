# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AriItem(scrapy.Item):
	img = scrapy.Field()
	status = scrapy.Field()
	client = scrapy.Field()
	category = scrapy.Field()
	sales_rep = scrapy.Field()
	supplier = scrapy.Field()
	companystreetAddress = scrapy.Field()
	companypostalCode = scrapy.Field()
	companyaddressLocality = scrapy.Field()
	companyaddressRegion = scrapy.Field()
	companyPhone = scrapy.Field()
	companysite = scrapy.Field()
	companyEmail = scrapy.Field()
	companyShortDescription = scrapy.Field()
	companyLongDescription = scrapy.Field()
	companyTitle = scrapy.Field()
	companysubTitle = scrapy.Field()




