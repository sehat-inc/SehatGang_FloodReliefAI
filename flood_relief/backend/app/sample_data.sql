-- Clear existing resources
TRUNCATE TABLE resources CASCADE;

-- Sindh Province (Major relief centers)
INSERT INTO resources (type, quantity, location) VALUES
    -- Karachi (Main distribution hub)
    ('boat', 50, ST_SetSRID(ST_MakePoint(67.0011, 24.8607), 4326)),
    ('food', 1000, ST_SetSRID(ST_MakePoint(67.0011, 24.8607), 4326)),
    ('shelter', 200, ST_SetSRID(ST_MakePoint(67.0011, 24.8607), 4326)),
    
    -- Hyderabad (Secondary hub)
    ('boat', 30, ST_SetSRID(ST_MakePoint(68.3577, 25.3960), 4326)),
    ('food', 800, ST_SetSRID(ST_MakePoint(68.3577, 25.3960), 4326)),
    ('shelter', 150, ST_SetSRID(ST_MakePoint(68.3577, 25.3960), 4326)),
    
    -- Sukkur (Strategic location for northern Sindh)
    ('boat', 40, ST_SetSRID(ST_MakePoint(68.8624, 27.7052), 4326)),
    ('food', 600, ST_SetSRID(ST_MakePoint(68.8624, 27.7052), 4326)),
    ('shelter', 120, ST_SetSRID(ST_MakePoint(68.8624, 27.7052), 4326));

-- Balochistan Province (Relief centers)
INSERT INTO resources (type, quantity, location) VALUES
    -- Quetta (Main hub)
    ('boat', 25, ST_SetSRID(ST_MakePoint(67.0099, 30.1798), 4326)),
    ('food', 500, ST_SetSRID(ST_MakePoint(67.0099, 30.1798), 4326)),
    ('shelter', 100, ST_SetSRID(ST_MakePoint(67.0099, 30.1798), 4326)),
    
    -- Gwadar (Coastal hub)
    ('boat', 20, ST_SetSRID(ST_MakePoint(62.3254, 25.1264), 4326)),
    ('food', 300, ST_SetSRID(ST_MakePoint(62.3254, 25.1264), 4326)),
    ('shelter', 80, ST_SetSRID(ST_MakePoint(62.3254, 25.1264), 4326));

-- Punjab Province (Strategic locations)
INSERT INTO resources (type, quantity, location) VALUES
    -- Multan (South Punjab hub)
    ('boat', 35, ST_SetSRID(ST_MakePoint(71.5249, 30.1575), 4326)),
    ('food', 700, ST_SetSRID(ST_MakePoint(71.5249, 30.1575), 4326)),
    ('shelter', 140, ST_SetSRID(ST_MakePoint(71.5249, 30.1575), 4326)),
    
    -- Lahore (Main distribution center)
    ('boat', 45, ST_SetSRID(ST_MakePoint(74.3587, 31.5204), 4326)),
    ('food', 900, ST_SetSRID(ST_MakePoint(74.3587, 31.5204), 4326)),
    ('shelter', 180, ST_SetSRID(ST_MakePoint(74.3587, 31.5204), 4326));

-- KPK Province (Relief points)
INSERT INTO resources (type, quantity, location) VALUES
    -- Peshawar (Main hub)
    ('boat', 30, ST_SetSRID(ST_MakePoint(71.5249, 34.0151), 4326)),
    ('food', 600, ST_SetSRID(ST_MakePoint(71.5249, 34.0151), 4326)),
    ('shelter', 120, ST_SetSRID(ST_MakePoint(71.5249, 34.0151), 4326)),
    
    -- Mingora (Swat Valley hub)
    ('boat', 25, ST_SetSRID(ST_MakePoint(72.3597, 34.7717), 4326)),
    ('food', 400, ST_SetSRID(ST_MakePoint(72.3597, 34.7717), 4326)),
    ('shelter', 90, ST_SetSRID(ST_MakePoint(72.3597, 34.7717), 4326));

/*
Resource Distribution Logic:

1. Boats:
- Larger quantities in coastal and riverine areas
- Karachi (50) and Sukkur (40) have most boats due to their proximity to water bodies
- Smaller quantities in inland cities

2. Food Packages:
- Each package serves a family of 5 for one week
- Larger quantities in major distribution hubs
- Karachi (1000) and Lahore (900) have the most as main distribution points

3. Shelter Units:
- Each unit can accommodate 4-5 families
- Distribution based on population density and accessibility
- More units in major cities for quick deployment

Strategic Placement:
- Resources are placed in cities with good road connectivity
- Coastal cities have more boats
- Major cities have larger quantities for redistribution
- Secondary hubs maintain moderate quantities for local response
*/
