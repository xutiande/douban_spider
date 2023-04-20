from scrapy import cmdline
# cmdline.execute('scrapy crawl db -o douban.csv'.split())            #直接安装setting中的表头格式创建csv文件
cmdline.execute('scrapy crawl db '.split())