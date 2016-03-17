#!coding:utf-8

import xlwt

def XlwtWrite(filename):
	xlsfile = xlwt.Workbook()
	sheet1 = xlsfile.add_sheet(u"sheet1",cell_overwrite_ok = True)
	keys = open("key.txt","r").readlines()
	hosts = open("host.txt","r").readlines()
	for i in range(0,len(keys)):
		print keys[i].decode("utf-8")
		sheet1.write(0,i,keys[i].decode("utf-8"))
	# print keys[0].decode("utf-8")
	print hosts
	hosts = [host.replace("\n","") for host in hosts]
	print hosts
	for i in range(1,len(hosts)):
		print hosts[i].decode("utf-8","ignore")
		sheet1.write(i,0,hosts[i].decode("utf-8","ignore"))
	xlsfile.save(filename)

if __name__ == "__main__":
	XlwtWrite("new.xls")	