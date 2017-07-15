#https://www.profootballfocus.com/nfl/teams/buffalo-bills/4/roster
from lxml import html
from lxml import etree
import requests

page = requests.get('https://www.profootballfocus.com/nfl/teams/buffalo-bills/4/roster')
tree = html.fromstring(page.content)
#print(etree.tostring(tree, pretty_print=True))


#This will create a list of buyers:
position = tree.xpath('//tr[@class="roster-header"]//td/text()')
#This will create a list of prices
#prices = tree.xpath('//span[@class="item-price"]/text()')
players = tree.xpath('//tr//td//a/text()')

print ('Positions: ', position)
print ('Players: ', players)

# elems = tree.xpath('//table[@class="table-draftmaster table-roster"]//tbody//tr/text()')
# print('Elements: ', elems)

for e in tree.xpath('//table[@class="table table-draftmaster table-roster table-responsive ui-table"]//tbody//tr//td/a'):
	print(e.text)