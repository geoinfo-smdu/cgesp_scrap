from datetime import timedelta, date

start_date = date(2017, 5, 1)
end_date = date(2017, 6, 2)

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

for single_date in daterange(start_date, end_date):
	# print(single_date.strftime("%Y-%m-%d"))
	year = single_date.strftime("%Y")
	month = single_date.strftime("%m")
	day = single_date.strftime("%d")
	# print(year,month,day)
	my_url="http://www.cgesp.org/v3/alagamentos.jsp?dataBusca="+day+"%2F"+month+"%2F"+year
	print(my_url)