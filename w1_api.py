import requests

class W1Api(object):
	def __init__(self, token):
		self.url = "https://api.w1.ru/OpenApi/"		
		self.headers = {"Authorization": "Bearer %s" % token, "Accept": "application/vnd.wallet.openapi.v1+json"}
		

	def balance(self):
		url = self.url + "balance"		
		return requests.get(url, headers = self.headers)

	def find_invoice(self, invoice_id = None, order_id = None):
		if invoice_id and order_id or not invoice_id and not order_id:
			raise Exception("Invalid invoice_id, order_id (%s, %s) pair" %
			 (invoice_id if invoice_id else "None", order_id if order_id else "None"))

		url = self.url + "invoices/" + ((invoice_id + "/operations") if invoice_id else "?orderId=%s" % order_id)				
		return requests.get(url, headers = self.headers)

	def find_payment(self, payment_id = None, external_id = None):
		if payment_id and external_id or not payment_id and not external_id:
			raise Exception("Invalid invoice_id, order_id (%s, %s) pair" %
			 (payment_id if payment_id else "None", external_id if external_id else "None"))

		url = self.url + "payments/" + (payment_id if payment_id else "?externalId=%s" % external_id)

		return requests.get(url, headers = self.headers)
