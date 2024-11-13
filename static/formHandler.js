document.addEventListener('DOMContentLoaded', () => {

    // Handle Add Athlete Form Submission
    document.getElementById('add-athlete-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = {
            Name: document.getElementById('name').value,
            Gender: document.getElementById('gender').value,
            Date_of_birth: document.getElementById('dob').value,
            Height: document.getElementById('height').value,
            Weight: document.getElementById('weight').value,
            Country_code: document.getElementById('country_code').value,
            Country: document.getElementById('country').value,
            Continent: document.getElementById('continent').value
        };

        try {
            const response = await fetch('/add_athlete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                window.location.href = '/';
            } else {
                alert(result.error);
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
            window.location.href = '/';
        }
    });

    // Handle Add Match Form Submission
    document.getElementById('add-match-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const matchDateInput = document.getElementById('match_date');
        const dateError = document.getElementById('date-error');
        const matchDate = new Date(matchDateInput.value);
        const minDate = new Date('2024-07-26');
        const maxDate = new Date('2024-08-11');

        if (matchDate < minDate || matchDate > maxDate) {
            dateError.style.display = 'inline';
            return;
        } else {
            dateError.style.display = 'none';
        }

        const matchData = {
            Athlete_Name: document.getElementById('athlete_name_match').value,
            Match_name: document.getElementById('match_name').value,
            Match_date: matchDateInput.value,
            Sport_name: document.getElementById('sport_name').value,
            Category: document.getElementById('category').value,
            Is_individual: document.getElementById('is_individual').value === 'true',
            Officials_Name: document.getElementById('officials_name').value,
            Position: document.getElementById('position').value,
            Medal_type: document.getElementById('medal_type').value,
            Venue_name: document.getElementById('venue_name').value,
            Address: document.getElementById('venue_address').value,
            Capacity: document.getElementById('venue_capacity').value
        };

        try {
            const response = await fetch('/add_match', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(matchData)
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                window.location.href = '/';
            } else {
                alert(result.error);
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
            window.location.href = '/';
        }
    });

    // Handle Delete Match Button Click
    document.querySelectorAll('.delete-match-button').forEach(button => {
        button.addEventListener('click', async (event) => {
            const athlete_pid = event.target.getAttribute('data-athlete-pid');
            const match_id = event.target.getAttribute('data-match-id');

            if (!athlete_pid || !match_id) {
                console.error("Missing athlete_pid or match_id");
                alert("Unable to delete: Missing athlete or match information.");
                return;
            }

            const confirmDelete = confirm('Are you sure you want to delete this match participation?');
            if (confirmDelete) {
                try {
                    const response = await fetch('/delete_match', {
                        method: 'DELETE',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ athlete_pid, match_id })
                    });
                    const result = await response.json();
                    if (response.ok) {
                        alert(result.message);
                        window.location.reload();
                    } else {
                        alert(result.error);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An unexpected error occurred. Please try again.');
                }
            }
        });
    });

    document.querySelectorAll('.edit-match-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const athlete_pid = event.target.getAttribute('data-athlete-pid');
            const match_id = event.target.getAttribute('data-match-id');
            const match_date = event.target.getAttribute('data-match-date'); // New Match Date
            const position = event.target.getAttribute('data-position');
            const medal_type = event.target.getAttribute('data-medal-type');
    
            // Populate the form with existing data
            document.getElementById('edit-athlete-pid').value = athlete_pid;
            document.getElementById('edit-match-id').value = match_id;
            document.getElementById('edit-match-date').value = match_date; // Set Match Date
            document.getElementById('edit-position').value = position;
            document.getElementById('edit-medal-type').value = medal_type;
    
            // Display the modal
            document.getElementById('edit-match-modal').style.display = 'block';
        });
    });
    
    // Handle Edit Match Form Submission
    document.getElementById('edit-match-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const matchDateInput = document.getElementById('edit-match-date');
        const dateError = document.getElementById('edit-date-error'); // Add a span for displaying errors
        const matchDate = new Date(matchDateInput.value);
        const minDate = new Date('2024-07-26');
        const maxDate = new Date('2024-08-11');

        // Validate match date
        if (matchDate < minDate || matchDate > maxDate) {
            dateError.style.display = 'inline'; // Show error message
            return;
        } else {
            dateError.style.display = 'none'; // Hide error message if valid
        }

        const athlete_pid = document.getElementById('edit-athlete-pid').value;
        const match_id = document.getElementById('edit-match-id').value;
        const match_date = matchDateInput.value; // Validated Match Date
        const position = document.getElementById('edit-position').value;
        const medal_type = document.getElementById('edit-medal-type').value;

        const updateData = {
            athlete_pid: athlete_pid,
            match_id: match_id,
            match_date: match_date,
            position: position,
            medal_type: medal_type
        };

        try {
            const response = await fetch('/update_match', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updateData)
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                window.location.reload();
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred. Please try again.');
        }
    });

    // Handle Closing the Modal
    document.getElementById('close-edit-modal').addEventListener('click', () => {
        document.getElementById('edit-match-modal').style.display = 'none';
    });
});
