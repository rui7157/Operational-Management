#!coding:utf-8
from api.query import dict_api
import xlwt
import os
from flask import url_for,make_response 
from . import tool
def savestream(self, stream):
		padding = '\x00' * (0x1000 - (len(stream) % 0x1000))
		self.book_stream_len = len(stream) + len(padding)
		self.__build_directory()
		self.__build_sat()
		self.__build_header()
		s = ""
		s = s + str(self.header)
		s = s + str(self.packed_MSAT_1st)
		s = s + str(stream)
		s = s + str(padding)
		s = s + str(self.packed_MSAT_2nd)
		s = s + str(self.packed_SAT)
		s = s + str(self.dir_stream)
		return s


@tool.route("/tool/query/download_excel")
def download_excel():
	urls = ""
	keys = ""
	dictdata = dict_api(urls, keys)
	str_data = generate_xls(dictdata)
	response = make_response(str_data)
	response.headers['Content-Type'] = 'application/vnd.ms-excel'
	response.headers['Content-Disposition'] = 'attachment; filename=bauduquery.xls'
	return response


def generate_xls(dictdata):
	xls_file = xlwt.Workbook()
	sheet = xls_file.add_sheet(u"百度排名",cell_overwrite_ok = True)
	urls = dictdata.keys()
	keys = dictdata.vlues()
	for k,v in dictdata.items():		
		sheet.write(k[i],1)
		v = v.splite("\n")
		for i in range(0,len(v)):
			sheet.write(1,v[i])
	stream = xls_file.get_biff_data()
	doc = XlsDoc()
	str_data = doc.savestream(stream)
	return str_data


# if __name__ == '__main__':
# 	urls = open('host.txt', 'rU').readlines()
# 	keys = open("key.txt", "rU").readlines()
# 	dictdata = api.query.dict_api(urls=urls, keys=keys)