# import modules
import os
import web
import json
import random

# Set urls
urls = (
	'/', 'index',
	'/api', 'api',
	'/api/madlibs', 'getMadlibs',
	'/api/madlibs/(\\d+)', 'getMadlib',
	'/api/(.*)', 'madlibCall'
)

# Set app and render
app = web.application(urls, globals())
render = web.template.render('templates/', base="layout")

# / Route
class index(object):
	def GET(self):
		return render.index(output = "", title = "")

	def POST(self):
		form = web.input()
		output = ""
		title = form["title"]
		for i in range(0, len(form)/2):
			v = "v" + str(i) if "v" + str(i) in form else ""
			b = "b" + str(i)
			if v in form:
				output += form[v]
			if b in form:
				output += form[b]
		return render.index(output = output, title = title)

# /api route
class api(object):
	def GET(self):
		return render.api()

# /api/madlibs route
class getMadlibs:
	def GET(self):
		# Set headers
		web.header("Access-Control-Allow-Origin", "*") # Allow all access
		web.header("Content-Type", "application/json") # Set content type

		# Load json data
		with open('data/templates.json') as data_file:
			data = json.load(data_file)
		data = data["templates"]

		# Get the template
		return json.dumps(data, indent=4)	# Send data

# /api/madlibs/{id} route
class getMadlib:
	def GET(self, id):
		# Set headers
		web.header("Access-Control-Allow-Origin", "*") # Allow all access
		web.header("Content-Type", "application/json") # Set content type

		# Fix up route parameter types
		id = int(id)

		# Load json data
		with open('data/templates.json') as data_file:
			data = json.load(data_file)
		data = data["templates"]

		# Check if elements exist
		data_count = len(data)
		if data_count < 1:
			return json.dumps({"error": "Invalid length range - No templates exist"})
		if id == 0 or data_count < id:
			return json.dumps({"error": "Invalid ID - That template doesn't exist"})

		index = id - 1

		# Get the template
		return json.dumps(data[index], indent=4)	# Send data

# /api/random route
class madlibCall(object):
	def GET(self, type):
		# Set headers
		web.header("Access-Control-Allow-Origin", "*") # Allow all access
		web.header("Content-Type", "application/json") # Set content type
		if (type == "random"):
			# Load json data
			with open('data/templates.json') as data_file:
				data = json.load(data_file)
			# Return the random template
			i = web.input(maxlength="100", minlength="0")
			maxlength = 100
			minlength = 0
			# Convert
			if i["maxlength"].isdigit():
				maxlength = int(i["maxlength"])
			if i["minlength"].isdigit():
				minlength = int(i["minlength"])
			if maxlength < minlength: # Can't have min greater than max!
				maxlength, minlength = minlength, maxlength # Swap variables
			print minlength, maxlength
			# Filter the data based on length
			new_data = [elem for elem in data["templates"] if (len(elem["blanks"]) <= maxlength and len(elem["blanks"]) >= minlength)]
			# Check if elements exist
			if len(new_data) < 1:
				return json.dumps({"error": "Invalid length range - No templates exist"})
			# Get a random index for the templates
			randomIndex = random.randint(0, len(new_data) - 1)
			return json.dumps(new_data[randomIndex], indent=4)	# Send data
		else:
			return json.dumps({"error": "Invalid API call"})

if __name__ == "__main__":
	app.run()
