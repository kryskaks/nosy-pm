import requests

class W1Api(object):
	def __init__(self, token):
		self.url = "https://api.w1.ru/OpenApi/"
		self.token = token	

	def balance(self):
		url = self.url + "balance"
		headers = {"Authorization": "Bearer %s" % self.token, "Accept": "application/vnd.wallet.openapi.v1+json"}			
		return requests.get(url, headers = headers)

	def find_invoice(self, invoice_id = None, order_id = None):
		if not invoice_id and not order_id:
			raise Exception("invoice_id or order_id must be set")

		if invoice_id and order_id or not invoice_id and not order_id:
			raise Exception("Invalid invoice_id, order_id (%s, %s) pair" %
			 (invoice_id if invoice_id else "None", order_id if order_id else "None"))

		url = self.url + "invoices/" + (invoice_id if invoice_id else "?orderId=%s" % order_id)		
		headers = {"Authorization": "Bearer %s" % self.token, "Accept": "application/vnd.wallet.openapi.v1+json"}			
		return requests.get(url, headers = headers)
