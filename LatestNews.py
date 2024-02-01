import http.server
import urllib.request
import re
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            url = 'https://time.com/'
            response = urllib.request.urlopen(url)
            data = response.read().decode('utf-8')

            extracted_data = []
            regex_outer = re.compile(r'<li class="latest-stories__item">(.*?)<\/li>', re.DOTALL)
            matches_outer = regex_outer.findall(data)

            if matches_outer:
                for match_outer in matches_outer:
                    regex_inner = re.compile(r'<a[^>]*href="([^"]*)"[^>]*>\s*<h3[^>]*>(.*?)<\/h3>\s*<\/a>', re.DOTALL)
                    match_inner = regex_inner.search(match_outer)
                    if match_inner:
                        href = match_inner.group(1)
                        h3_content = match_inner.group(2).strip() if match_inner.group(2) else ''
                        extracted_data.append({
                            'title': h3_content,
                            'link': href
                        })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(extracted_data).encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == '__main__':
    port = 4000
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print(f'Server is running on http://localhost:{port}')
    httpd.serve_forever()
