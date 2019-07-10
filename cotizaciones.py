from bs4 import BeautifulSoup as bs
import requests
import sqlalchemy

# Retorna un array con las cotizaciones del dia
def getCotizaciones():
	url = "https://www.brou.com.uy/c/portal/render_portlet?p_l_id=20593&p_p_id=cotizacionfull_WAR_broutmfportlet_INSTANCE_otHfewh1klyS"
	r = requests.get(url)
	soup = bs(r.text, 'html.parser')
	tbody = soup.find('tbody')
	array = []
	
	for moneda in tbody.findAll('tr'):
		array.append({ 
			"moneda" : moneda.find('p',{"class":"moneda"}).string,
			"compra" : moneda.findAll('p',{"class":"valor"})[0].string.replace('.','').replace(',','.').replace('-','').strip(),
			"venta"  : moneda.findAll('p',{"class":"valor"})[1].string.replace('.','').replace(',','.').replace('-','').strip()
		})

	return array

def insertCotizaciones(data):
	dbUrl = 'postgresql://postgres:p4ssw0rd@localhost:5432/cotizaciones'
	engine = sqlalchemy.create_engine(dbUrl)
	con = engine.connect()

	for elemento in data:
		if elemento['compra'] == '':
			statement = sqlalchemy.sql.text(""" insert into monedas(moneda, compra, venta) values(:moneda, NULL, :venta)""")	
		elif elemento['venta'] == '':
			statement = sqlalchemy.sql.text(""" insert into monedas(moneda, compra, venta) values(:moneda, :compra, NULL )""")
		else:
			statement = sqlalchemy.sql.text(""" insert into monedas(moneda, compra, venta) values(:moneda, :compra, :venta)""")	
		con.execute(statement, **elemento)



array = getCotizaciones()
insertCotizaciones(array)
