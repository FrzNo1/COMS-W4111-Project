## Endpoints

### Database 
- The PostgreSQL account name: rf2715

### URL of web application
```bash
http://34.73.166.195:8111
```

### GET `/retrieve_athlete_info`
- Retrieves the athlete and all his/her related information for the given name.
- Example Request:
```bash
http://34.73.166.195:8111/retrieve_atretrieve_athlete_info?name=Weikeng
```
- Example Response:
```json
{
    "name": "Weikeng Liang",
    "gender": "male",
    "date_of_birth": "datetime.date(2000, 11, 30)",
    "match_name": "badminton_mens_double_final",
    "position": 2,
    "medal_type": "Silver",
    "country": "CHN",
    "coach": "Qiqiu Chen",
    "athlete_pid": 43,
    "match_id": 12,
    "venue_name": "porte de la chapelle arena"
}
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
    "Venue_name": "TEST",
    "Address": "TEST",
    "Capacity": "100",
	"Officials_Name": "METSPALU Iris",
	"Position": "1",
	"Medal_type": "Silver"
}
```
- Example Response:
```json
{
    "Match_name": "TEST",
    "message": "Match added successfully"
}
```
- Returns a 400 error if one of the information related to the match is not given.
- Returns a 400 error if match already exists.
- Returns a 400 error if there is no matching athlete in the database
- Returns a 400 error if there is no matching official in the database
- Returns a 201 on success.

### DELETE `/delete_match`
- Deletes a match participation entry for a given athlete and match ID.
- Example Request:
```json
{
    "athlete_pid": 43,
    "match_id": 12
}
```
- Example Response:
```json
{
    "message": "Match participation deleted successfully"
}
```
- Returns a 400 error if athlete PID or match ID is not provided.
- Returns a 404 error if no matching entry is found.
- Returns a 200 on success.

### PUT `/update_match`

- Updates match details, including match date, position, and medal type for a given athlete and match.
- Example Request:
```json
{
    "athlete_pid": 43,
    "match_id": 12,
    "match_date": "2024-08-06",
    "position": "2",
    "medal_type": "Bronze"
}
```
- Example Response:
```json
{
    "message": "Match updated successfully"
}
```
- Returns a 400 error if any required information is missing.
- Returns a 404 error if no matching entry is found.
- Returns a 200 on success.

### Implementation from Part 1

We implement the functionality we described from part 1
- Create: Users can simply add new athletes and add new matches. The backend will handle all the logics to update all the tables.
- Read: User can search for an athlete. All athletes and related matches' information will be displayed accordingly.
- Update: User can update the athlete and match information. They can change the date and athletes' ranks for the match.
- Delete: User is able to delete the athlete or match information.

### Interesting database operations 

- Athlete Search page
    - This page allows users to search for athletes by name and view detailed information about them, including personal details, match participations, positions, medals won, associated coaches, and venues.
    - The application executes a complex SQL query that joins multiple tables—Person, Athletes, Participate, Matches_Sports, Hold, Venues, Comefrom, and Train—to gather comprehensive information about the athlete.
    - This page demonstrates the power of relational databases in aggregating and presenting interconnected data from multiple tables. 

- Add Match Participation Page
    - This page enables users to add new match participation records for athletes, including details about the match, sport, officials, venue, and the athlete's performance.
    - The application checks for the existence of records in related tables (Sports, Venues) and inserts new records if they don't already exist.
    - This page highlights the complexity of maintaining data integrity and consistency across multiple related tables. 

### AI Using
- Use ChatGPT to generates frontend drop-down boxes for any input elements.

## Running the Service
Make sure you have Python 3 and `pip` installed on your machine and clone the repository.
```bash
cd ~/COMS-W4111-Project
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

