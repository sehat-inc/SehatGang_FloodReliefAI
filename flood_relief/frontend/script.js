document.getElementById('demandForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    // Convert numeric fields from string to number
    data.latitude = parseFloat(data.latitude);
    data.longitude = parseFloat(data.longitude);
    data.quantity = parseInt(data.quantity);
    data.priority = parseInt(data.priority);

    // Validate conversions
    if (isNaN(data.latitude) || isNaN(data.longitude) || isNaN(data.quantity) || isNaN(data.priority)) {
        alert("Please provide valid numeric inputs");
        return;
    }

    console.log("Payload:", data); // Debug log

    // Updated URL to point to the backend server
    const response = await fetch('http://localhost:8000/demands/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        alert('Demand submitted successfully!');
        event.target.reset();
    } else {
        alert('Failed to submit demand.');
    }
});
