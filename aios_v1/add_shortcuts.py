import frappe
import json

def execute():
    # Cek Web Link untuk Client
    if not frappe.db.exists('Web Link', 'AIOS Client Portal'):
        doc = frappe.new_doc('Web Link')
        doc.label = 'AIOS Client Portal'
        doc.url = '/'
        doc.insert(ignore_permissions=True)
    
    # Cek Web Link untuk Developer
    if not frappe.db.exists('Web Link', 'AIOS Developer Portal'):
        doc = frappe.new_doc('Web Link')
        doc.label = 'AIOS Developer Portal'
        doc.url = '/developer'
        doc.insert(ignore_permissions=True)
        
    print('Links added!')
