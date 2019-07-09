from bs4 import BeautifulSoup as bs
import requests

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




print (getCotizaciones())
