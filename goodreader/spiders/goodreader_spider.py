from scrapy import Spider
from scrapy.http import Request

class GoodreaderSpiderSpider(Spider):
    name = 'goodreader_spider'
    allowed_domains = ['goodreads.com']
    start_urls = ['http://www.goodreads.com/quotes']


    def parse(self, response):
    	next_page = response.xpath('//*[@class="next_page"]/@href').extract_first()
    	absolute_next_page = response.urljoin(next_page)
    	yield Request((absolute_next_page))

    	qoutes_details= response.xpath('//*[@class="quoteDetails"]')
    	for qoutes_detail in qoutes_details:
	        author_name = qoutes_detail.xpath('.//*[@class="authorOrTitle"]/text()').extract_first()
	        author_url = qoutes_detail.xpath('.//*[@class="authorOrTitle"]/@href').extract_first()
	        absolute_author_url = response.urljoin(author_url)
	        yield Request((absolute_author_url), callback=self.parse_goodreader_author)

	        author_img = qoutes_detail.xpath('.//*[@class="leftAlignedImage"]/img/@src').extract_first()
	        qoute = qoutes_detail.xpath('.//*[@class="quoteText"]/text()').extract_first()
	        view_this_qoute_count = qoutes_detail.xpath('.//*[@title="View this quote"]/text()').extract_first()
	        view_this_qoute_url = qoutes_detail.xpath('.//*[@title="View this quote"]/@href').extract_first()
    		view_this_qoute_absolute_url= response.urljoin(view_this_qoute_url)
	        tags_names_list = qoutes_detail.xpath('.//*[@class="greyText smallText left"]/a/text()').extract()
	        tags_names_string = "|".join(tags_names_list)
	        tags_urls_list = qoutes_detail.xpath('.//*[@class="greyText smallText left"]/a/@href').extract()
	        tags_urls_string = "|".join(tags_urls_list)
	        yield{ 'tags_urls_string':tags_urls_string,
	        		'tags_names_string':tags_names_string,
	        		'author_name':author_name,
	        		'qoute':qoute,
	        		'absolute_author_url':absolute_author_url,
	        		'absolute_next_page':absolute_next_page,
	        		'author_img':author_img,
	        		'view_this_qoute_count':view_this_qoute_count,
	        		'view_this_qoute_absolute_url':view_this_qoute_absolute_url }

	        tags = qoutes_detail.xpath('.//*[@class="greyText smallText left"]/a')
	        for tag in tags:
	        	tages_url  = tag.xpath('./@href').extract_first()
		        absolute_tages_url = response.urljoin(tages_url)
		        yield Request((absolute_tages_url))
    	

		
    	main_tages = response.xpath('//*[@class="gr-hyperlink"]')
    	for main_tag in main_tages:
    		main_tage_name= main_tag.xpath('./text()').extract_first()
    		main_tage_url=  main_tag.xpath('./@href').extract_first()
    		main_tag_absolute_url= response.urljoin(main_tage_url)
	    	yield Request((main_tag_absolute_url))

    def parse_goodreader_author(self, response):
    	all_author_qoute_url= response.xpath('//*[@style="text-align: right;"]/a/@href').extract_first()
    	absolute_url = response.urljoin(all_author_qoute_url)
    	yield Request((absolute_url))
