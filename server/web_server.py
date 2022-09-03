from http.server import HTTPServer, SimpleHTTPRequestHandler
import psycopg2
import sys
import os


HOST_NAME = "0.0.0.0"
PORT = 8080

conn = psycopg2.connect(
	host=os.getenv('HOST'),
	database=os.getenv('DATABASE'),
	user=os.getenv('USER'),
	password=os.getenv('PASSWORD'),
	port=os.getenv('PORT'),
)
cursor = conn.cursor()

class PythonServer(SimpleHTTPRequestHandler):
	def do_GET(self):
		'''Handling GET request and replacing {{content}} in html template'''
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')) as file:
			file = file.read()
		cursor.execute("SELECT location, url, title, images FROM sreality.public.flats;")
		flats = cursor.fetchall()
		table_row = ""
		for flat in flats:
			table_row += f'''
			<div class="row align-items-center">
				<div class="col text-start">
					<div class="row">
						<h1><a href="{flat[1]}">{flat[2]}</a></h1>
					</div>
					<div class="row">
						<h2>{flat[0]}</h2>
					</div>
				</div>
				<div class="col">
					<div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
						<div class="carousel-inner text-start">
							{chr(10).join([f"""
							<div class="carousel-item active">
								<img src="{url}"
									class="d-block img-thumbnail" alt="{flat[2]}">
							</div>""" for url in flat[3]]).replace('active', '', len(flat[3])-1)}
						</div>
						<button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls"
							data-bs-slide="prev">
							<span class="carousel-control-prev-icon" aria-hidden="true"></span>
							<span class="visually-hidden">Previous</span>
						</button>
						<button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls"
							data-bs-slide="next">
							<span class="carousel-control-next-icon" aria-hidden="true"></span>
							<span class="visually-hidden">Next</span>
						</button>
					</div>
				</div>
			</div>'''
		file = file.replace("{{content}}", table_row)
		self.send_response(200, "OK")
		self.end_headers()
		self.wfile.write(bytes(file, "utf-8"))

if __name__ == "__main__":
	server = HTTPServer((HOST_NAME, PORT), PythonServer)
	print(f"Server started http://{HOST_NAME}:{PORT}")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		server.server_close()
		cursor.commit()
		conn.commit()
		conn.close()
		print("Server stopped successfully")
		sys.exit(0)
