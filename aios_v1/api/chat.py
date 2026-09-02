import frappe
from werkzeug.wrappers import Response
import json

def handle_chat_request():
    path = frappe.request.path
    if not path.startswith('/api/chat/'):
        return
        
    parts = path.split('/')
    if len(parts) >= 4:
        branch = parts[3]
        action = parts[4] if len(parts) > 4 else None
        
        # Intercept POST /api/chat/<branch>/stream
        if action == 'stream' and frappe.request.method == 'POST':
            def generate():
                yield f"data: {json.dumps({'type': 'meta', 'conversationId': 999})}\n\n"
                yield f"data: {json.dumps({'type': 'delta', 'text': f'Test koneksi sukses! Pesan ini dikirim langsung dari Frappe Python untuk branch: {branch.upper()}.'})}\n\n"
                yield f"data: {json.dumps({'type': 'done', 'conversationId': 999, 'delegatedTo': 'None', 'dataUsed': [], 'limitation': '', 'tokens': 10})}\n\n"
            
            frappe.local.response = Response(generate(), mimetype='text/event-stream')
            frappe.local.response.headers.add('Cache-Control', 'no-cache, no-transform')
            frappe.local.response.headers.add('Connection', 'keep-alive')
            return
