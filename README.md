## Endpoints

### GET `/retrieve_athlete_info/<athlete_name>`
- Retrieves the athlete and all his/her related information for the given name.
- Example Request:
```bash
http://34.139.156.199:8111/retrieve_athlete_info/Weikeng
```
- Example Response:
```json
{'name': 'Weikeng Liang', 'gender': 'male', 'date_of_birth': datetime.date(2000, 11, 30), 'match_name': "badminton_men's_double_final", 'position': 2, 'medal_type': 'Silver', 'country': 'CHN', 'coach': 'Qiqiu Chen'}
```
- Returns a 400 error if name is not given.
- Returns a 404 error if name does not exist in the athlete database.
- Returns a 201 on success.


### POST `/add_athlete`
- Add athlete to the database given his/her information
- Example Request:
```json
{
	"Name": "TEST",
	"Gender": "Female",
	"Date_of_birth": "1995-06-15",
	"Height": 1.70,
	"Weight": 65.5,
	"Country_code": "TTT",
	"Country": "Test",
	"Continent": "North America"
}
```
- Example Response:
```json
{
    "message": "Athlete added successfully",
    "pid": 43
}
```
- Returns a 400 error if one of the information related to athlete is not given.
- Returns a 400 error if athlete already exists.
- Returns a 201 on success.


### POST `/add_match`
- Add match to the database given its information
- IMPORTANT: Official has to be pre existed in the database
- Example Request:
```json
{
	"Athlete_Name": "TEST",
	"Match_name": "TEST",
	"Match_date": "2024-08-05",
	"Sport_name": "TEST",
	"Category": "TEST",
	"Is_individual": true,
	"Officials_Name": "METSPALU Iris",
	"Position": "1",
	"Medal_type": "Silver"
}
```
- Example Response:
```json
{
    "Match_name": "TEST",
    "message": "Athlete added successfully"
}
```
- Returns a 400 error if one of the information related to the match is not given.
- Returns a 400 error if match already exists.
- Returns a 400 error if there is no matching athlete in the database
- Returns a 400 error if there is no matching official in the database
- Returns a 201 on success.



## Running the Service
Make sure you have Python 3 and `pip` installed on your machine and clone the repository.
```bash
cd ~/part3
```
Create a virtual environment and install the dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```
Run the application from the root directory.
```bash
python3 server.py
```
The application will be running on `http://localhost:8111/`.