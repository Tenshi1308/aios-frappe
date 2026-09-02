import frappe
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
import json
import traceback

def main():
    frappe.init(site='aios.localhost', sites_path='sites')
    frappe.connect()
    builder = EnvironBuilder(
        path='/api/auth/login',
        method='POST',
        headers={'Host': 'client.aios.localhost:8000', 'Origin': 'http://client.aios.localhost:8000'},
        data=json.dumps({'email': 'client@demo.id', 'password': 'client123'}),
        content_type='application/json'
    )
    env = builder.get_environ()
    req = Request(env)
    frappe.request = req
    frappe.local.request = req
    
    from aios_v1.api.dispatcher import handle_api_request, CustomAPIResponse
    try:
        handle_api_request()
        print("No response raised")
    except CustomAPIResponse as c:
        print("CustomAPIResponse raised successfully:", c.get_response().status_code, c.get_response().get_data(as_text=True))
    except Exception as e:
        print("Unexpected error:")
        traceback.print_exc()

if __name__ == '__main__':
    main()
