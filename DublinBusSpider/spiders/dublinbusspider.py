from scrapy.spider import Spider
from scrapy.selector import Selector
from datetime import datetime, time


class DublinBusSpider(Spider):
    name="dublinbusspider"
    allowed_domains=['http://www.dublinbus.ie/']

    def __init__(self, stop_number=None, *args, **kwargs):
        super(DublinBusSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.dublinbus.ie/en/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery=%s' % stop_number]

    def parse(self, response):
        hxs = Selector(response)

        now = datetime.now()
        now_time = now.time()
        if now_time >= time(00,00) and now_time <= time(06,00):
            page_elmnt = "//div[@id='stop-detail']"
        else:
            page_elmnt = "//table[@id='rtpi-results']"

        """realtime_table = hxs.xpath(page_elmnt).extract()"""
        realtime_table = hxs.xpath(page_elmnt).css('tr td').extract()
        print(realtime_table)

        Html_file= open("bustimes.html","w")
        Html_file.write("<html><body>")
        count=1
        for item in realtime_table:
            if (count%4 != 0):
                Html_file.write("%s" % item)
            Html_file.write("<br />")
            count=count+1

        Html_file.write("</body></html>")
        Html_file.close()



