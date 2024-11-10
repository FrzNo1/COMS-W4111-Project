
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
	python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
	# accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort
from flask import jsonify
from datetime import datetime


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://user:password@104.196.222.236/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@104.196.222.236/proj1part2"
#
DATABASEURI = "postgresql://rf2715:12345@104.196.222.236/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
conn = engine.connect()

# The string needs to be wrapped around text()

conn.execute(text("""CREATE TABLE IF NOT EXISTS test (
	id serial,
	name text
);"""))
conn.execute(text("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');"""))

# To make the queries run, we need to add this commit line

conn.commit() 

@app.before_request
def before_request():
	"""
	This function is run at the beginning of every web request
	(every time you enter an address in the web browser).
	We use it to setup a database connection that can be used throughout the request.

	The variable g is globally accessible.
	"""
	try:
		g.conn = engine.connect()
	except:
		print("uh oh, problem connecting to database")
		import traceback; traceback.print_exc()
		g.conn = None

@app.teardown_request
def teardown_request(exception):
	"""
	At the end of the web request, this makes sure to close the database connection.
	If you don't, the database could run out of memory!
	"""
	try:
		g.conn.close()
	except Exception as e:
		pass


@app.route('/retrieve_athlete_info/<name>', methods=['GET'])
def retrieve_athlete_info(name):
	"""
	Retrieves information about a person (athlete) based on the name provided via GET request.
	Example URL: http://localhost:8111/retrieve_athlete_info/Weikeng
	"""
	print(f"Searching for athlete with name: {name}")

	if not name:
		return "Error: No name provided in the request.", 400

	query = text("""
		WITH AthleteInfo AS (
			SELECT P.Name, P.Gender, P.Date_of_birth, A.PID AS Athlete_PID
			FROM Person P 
			JOIN Athletes A ON P.PID = A.PID
			WHERE P.Name LIKE :name
		),
		AthleteParticipation AS (
			SELECT AI.Name, AI.Gender, AI.Date_of_birth, P.Match_name, P.Position, P.Medal_type, AI.Athlete_PID
			FROM AthleteInfo AI JOIN Participate P ON AI.Athlete_PID = P.Athlete_PID
		)
		SELECT AP.Name, AP.Gender, AP.Date_of_birth, AP.Match_name, AP.Position, AP.Medal_type, C.Country_code, Co.Name AS Coach_Name
		FROM AthleteParticipation AP
		LEFT JOIN Comefrom C ON AP.Athlete_PID = C.PID
		LEFT JOIN Train T ON AP.Athlete_PID = T.Athlete_PID
		LEFT JOIN Person Co ON T.Coach_PID = Co.PID 
	""")

	cursor = g.conn.execute(query, {'name': f"%{name}%"})

	results = cursor.fetchall()
	if not results:
		return f"No athlete found with the name {name}.", 404  # Not found

	athlete_info = []
	for result in results:
		athlete_info.append({
			'name': result[0],           # Athlete's Name
			'gender': result[1],         # Athlete's Gender
			'date_of_birth': result[2],  # Athlete's Date of Birth
			'match_name': result[3],     # Match Name
			'position': result[4],       # Athlete's Position in the match
			'medal_type': result[5],      # Medal Type (e.g., Gold, Silver, Bronze)
			'country': result[6],
			'coach': result[7]
		})

	cursor.close()

	context = dict(data=athlete_info)
	return render_template("athlete_index.html", **context)


@app.route('/add_athlete', methods=['POST'])
def add_athlete():
	data = request.get_json()

	if not all(key in data for key in ['Name', 'Gender', 'Date_of_birth', 'Height', 'Weight', 'Country_code', 'Country', 'Continent']):
		return jsonify({'error': 'Missing required fields, please see documentation'}), 400

	name = data['Name']

	query = text("""
		SELECT PID 
		FROM Person 
		WHERE Name = :name
	""")
	result = g.conn.execute(query, {'name': name}).fetchone()

	if result:
		return jsonify({'error': 'Athlete with this name already exists'}), 400

	try:
		gender = data['Gender']
		date_of_birth = datetime.strptime(data['Date_of_birth'], '%Y-%m-%d')  # Assuming date is in YYYY-MM-DD format
		height = float(data['Height'])
		weight = float(data['Weight'])
		country_code = data['Country_code']
		country = data['Country']
		continent = data['Continent']

		# Person table
		query_max_pid = text("""
			SELECT COALESCE(MAX(CAST(PID AS INTEGER)), 0) + 1 
			FROM Person
		""")
		result = g.conn.execute(query_max_pid)
		next_pid = result.fetchone()[0]

		query = text("""
			INSERT INTO Person (PID, Name, Gender, Date_of_birth)
			VALUES (:pid, :name, :gender, :dob)
		""")
		g.conn.execute(query, {'pid': next_pid, 'name': name, 'gender': gender, 'dob': date_of_birth})

		print(f"DEGUG: Person table finished")

		# Athletes table
		query = text("""
			INSERT INTO Athletes (PID, Height, Weight)
			VALUES (:pid, :height, :weight)
		""")
		g.conn.execute(query, {'pid': next_pid, 'height': height, 'weight': weight})

		print(f"DEGUG: Athletes table finished")

		# Country table
		query = text("""
			SELECT Country_code 
			FROM Country 
			WHERE Country_code = :country_code
		""")
		result = g.conn.execute(query, {'country_code': country_code}).fetchone()
		if not result:
			query = text("""
				INSERT INTO Country (Country_code, Country, Continent)
				VALUES (:country_code, :country, :continent)
			""")
			g.conn.execute(query, {'country_code': country_code, 'country': country, 'continent': continent})

		print(f"DEGUG: Country table finished")

		# Comefrom table
		query = text("""
			INSERT INTO Comefrom (PID, Country_code)
			VALUES (:pid, :country_code)
		""")
		g.conn.execute(query, {'pid': next_pid, 'country_code': country_code})
		g.conn.commit()

		print(f"DEGUG: Comefrom table finished")

		g.conn.commit()
		return jsonify({'message': 'Athlete added successfully', 'pid': next_pid}), 201

	except Exception as e:
		# Handle errors gracefully
		return jsonify({'error': str(e)}), 500


@app.route('/add_match', methods=['POST'])
def add_match():
	data = request.get_json()

	if not all(key in data for key in ['Athlete_Name', 'Match_name', 'Match_date', 'Sport_name', 'Category', 'Is_individual', 'Officials_Name', 'Position', 'Medal_type']):
		return jsonify({'error': 'Missing required fields, please see documentation'}), 400

	match_name = data['Match_name']
	athlete_name = data['Athlete_Name']
	official_name = data['Officials_Name']
	sport_name = data['Sport_name']
	match_date = data['Match_date']
	category = data['Category']
	is_individual = data['Is_individual']
	position = data['Position']
	medal_type = data['Medal_type']

	query = text("""
		SELECT Match_name 
		FROM Matches_Sports 
		WHERE Match_name = :name
	""")
	result = g.conn.execute(query, {'name': match_name}).fetchone()
	if result:
		return jsonify({'error': 'Match with this name already exists'}), 400

	query = text("""
		SELECT p.PID 
		FROM Person P JOIN Athletes A ON P.PID = A.PID
		WHERE P.Name = :name
	""")
	result = g.conn.execute(query, {'name': athlete_name}).fetchone()
	if not result:
		return jsonify({'error': 'Athlete does not found. You need to /add_athlete to add athlete first'}), 400
	athlete_pid = result[0]

	query = text("""
		SELECT p.PID 
		FROM Person P JOIN Officials O ON P.PID = O.PID
		WHERE P.Name = :name
	""")
	result = g.conn.execute(query, {'name': official_name}).fetchone()
	if not result:
		return jsonify({'error': 'Official does not found. You need to provide the correct Officials names'}), 400
	official_pid = result[0]

	print(f"DEGUG: Start")

	try:
		# Sports Table
		query = text("""
			SELECT Sport_name 
			FROM Sports
			WHERE Sport_name = :name
		""")
		result = g.conn.execute(query, {'name': sport_name}).fetchone()
		if not result:
			query = text("""
				INSERT INTO Sports (Sport_name, Category, is_individual)
				VALUES (:sport_name, :category, :is_individual)
			""")
			g.conn.execute(query, {'sport_name': sport_name, 'category': category, 'is_individual': is_individual})

		print(f"DEGUG: Sports Table")

		# Matches_Sports Table
		insert_matches_sports_query = text("""
			INSERT INTO Matches_Sports (Match_name, Match_date, Sport_name)
			VALUES (:match_name, :match_date, :sport_name)
		""")
		g.conn.execute(insert_matches_sports_query, {'match_name': match_name,'match_date': match_date, 'sport_name': sport_name})

		print(f"DEGUG: Matches_Sports Table")

		# Participate Table
		insert_participate_query = text("""
			INSERT INTO Participate (Athlete_PID, Match_name, Position, Medal_type)
			VALUES (:athlete_pid, :match_name, :position, :medal_type)
		""")
		g.conn.execute(insert_participate_query, {'athlete_pid': athlete_pid, 'match_name': match_name, 'position': position, 'medal_type': medal_type})

		print(f"DEGUG: Participate Table")

		# Oversee Table
		insert_oversea_query = text("""
			INSERT INTO Oversee (Official_PID, Match_name)
			VALUES (:official_pid, :match_name)
		""")
		g.conn.execute(insert_oversea_query, {'official_pid': official_pid, 'match_name': match_name})

		print(f"DEGUG: Oversee Table")

		g.conn.commit()
		return jsonify({'message': 'Athlete added successfully', 'Match_name': match_name}), 201


	except Exception as e:
		# Handle errors gracefully
		return jsonify({'error': str(e)}), 500

	
if __name__ == "__main__":
	import click

	@click.command()
	@click.option('--debug', is_flag=True)
	@click.option('--threaded', is_flag=True)
	@click.argument('HOST', default='0.0.0.0')
	@click.argument('PORT', default=8111, type=int)
	def run(debug, threaded, host, port):
		"""
		This function handles command line parameters.
		Run the server using:

			python3 server.py

		Show the help text using:

			python3 server.py --help

		"""

		HOST, PORT = host, port
		print("running on %s:%d" % (HOST, PORT))
		app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

	run()
