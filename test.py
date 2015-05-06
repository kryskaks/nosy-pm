from pysimplesoap.client import SoapClient
from datetime import datetime
import requests

test_merchant_id = 129400107178
test_token = "f1bebd19-3d7a-46d1-b2da-25368651d076"
client_id = "test.ts"

def main():
	"Hello, world!"
	test()

def test():
	url = "https://api.w1.ru/OpenApi/balance"
	headers = {"Authorization": "Bearer %s" % test_token, "Accept": "application/vnd.wallet.openapi.v1+json"}	
	response = requests.get(url, headers = headers)
	print response
	print response.text
	return response

def test_soap_api():
	client = SoapClient(wsdl = "https://merchant.w1.ru/checkout/service.asmx?wsdl", trace = True)
	utcnow = datetime.utcnow()
	
	response = client.GetBalance(MerchantId = test_merchant_id, RequestDate = datetime.utcnow())
	print response		

if __name__ == '__main__':
	main()