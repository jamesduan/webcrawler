

from request_sender import send_request


print send_request('http://localhost:8888/upload_html', 'POST', "{'name' : 'jamesduan'}").body

