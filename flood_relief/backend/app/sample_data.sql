
-- Insert Resources
INSERT INTO resources (type, quantity, location) VALUES
    ('boat', 10, ST_SetSRID(ST_MakePoint(67.0011, 24.8607), 4326)),    -- Karachi
    ('shelter', 20, ST_SetSRID(ST_MakePoint(73.0479, 33.6844), 4326)), -- Islamabad
    ('food', 100, ST_SetSRID(ST_MakePoint(74.3587, 31.5204), 4326)),   -- Lahore
    ('boat', 5, ST_SetSRID(ST_MakePoint(71.5249, 30.1575), 4326)),     -- Multan
    ('shelter', 15, ST_SetSRID(ST_MakePoint(73.1321, 31.4504), 4326)), -- Faisalabad
    ('food', 50, ST_SetSRID(ST_MakePoint(68.3577, 25.3960), 4326));    -- Hyderabad

-- To test the API, you can use these cities and their corresponding resource types:

/*
Test Data for API requests:

1. Karachi:
{
    "type": "boat",
    "quantity": 2,
    "priority": 1,
    "city": "Karachi, Pakistan"
}

2. Islamabad:
{
    "type": "shelter",
    "quantity": 5,
    "priority": 2,
    "city": "Islamabad, Pakistan"
}

3. Lahore:
{
    "type": "food",
    "quantity": 20,
    "priority": 3,
    "city": "Lahore, Pakistan"
}

4. Multan:
{
    "type": "boat",
    "quantity": 1,
    "priority": 1,
    "city": "Multan, Pakistan"
}

5. Faisalabad:
{
    "type": "shelter",
    "quantity": 3,
    "priority": 2,
    "city": "Faisalabad, Pakistan"
}

6. Hyderabad:
{
    "type": "food",
    "quantity": 10,
    "priority": 4,
    "city": "Hyderabad, Pakistan"
}
*/
