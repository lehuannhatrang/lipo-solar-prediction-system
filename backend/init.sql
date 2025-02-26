-- Create database 
CREATE DATABASE prediction_core; 

-- Switch to the newly created database
\c prediction_core;

-- Create table for Li-ion Battery Status if it doesn't exist
CREATE TABLE IF NOT EXISTS liion_battery_status (
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Primary key using UUID
    battery_id VARCHAR(255), -- Battery ID (string, not unique)
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,      -- Timestamp
    voltage FLOAT,        -- Battery voltage (V)
    current FLOAT,        -- Charge/discharge current (A)
    state_of_charge FLOAT, -- State of Charge (SOC)
    state_of_health FLOAT, -- State of Health (SOH)
    temperature FLOAT,    -- Temperature (°C)
    impedance FLOAT,      -- Impedance/Resistance (Ω)
    charge_discharge_cycles INT, -- Charge/Discharge Cycles
    energy FLOAT,         -- Energy (Wh)
    cycle_time FLOAT,     -- Cycle Time (s)
    capacity FLOAT        -- Capacity (Ah)
);

--- Init data

DO $$ 
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO liion_battery_status (
            entity_id, 
            battery_id,
            ts, 
            voltage, 
            current, 
            state_of_charge, 
            state_of_health, 
            temperature, 
            impedance, 
            charge_discharge_cycles, 
            energy, 
            cycle_time, 
            capacity
        ) 
        VALUES (
            gen_random_uuid(), -- Generates a random UUID for entity_id
            'BAT' || LPAD(i::TEXT, 1, '0'),
            CURRENT_TIMESTAMP - (random() * interval '30 day'), -- Timestamp
            3.7 + random() * 0.2, -- Random voltage between 3.7 and 3.9 V
            1.0 + random() * 0.5, -- Random current between 1.0 and 1.5 A
            50.0 + random() * 50.0, -- Random SOC between 50% and 100%
            80.0 + random() * 20.0, -- Random SOH between 80% and 100%
            20.0 + random() * 10.0, -- Random temperature between 20°C and 30°C
            0.01 + random() * 0.05, -- Random impedance between 0.01Ω and 0.06Ω
            200 + floor(random() * 1000), -- Random charge/discharge cycles between 200 and 1200
            100.0 + random() * 50.0, -- Random energy between 100 Wh and 150 Wh
            1800 + floor(random() * 3600), -- Random cycle time between 1800 and 5400 seconds
            2.0 + random() * 3.0 -- Random capacity between 2 Ah and 5 Ah
        );
    END LOOP;
END $$;

-- Create table for solar_panel_battery_status if it doesn't exist
CREATE TABLE IF NOT EXISTS solar_panel_battery_status (
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Generate a random UUID as the primary key
    panel_id VARCHAR(255),
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Timestamp column with default current time
    solar_irradiance FLOAT, -- Solar Irradiance (W/m²)
    ambient_temperature FLOAT, -- Ambient Temperature (°C)
    module_temperature FLOAT, -- Module Temperature (°C)
    wind_speed FLOAT, -- Wind Speed (m/s)
    energy_output FLOAT, -- Energy Output (Wh)
    voltage FLOAT, -- Voltage (V)
    current FLOAT, -- Current (A)
    power_output FLOAT, -- Power Output (W)
    state_of_charge FLOAT, -- Battery State of Charge (SOC) in percentage, optional
    inverter_efficiency FLOAT -- Inverter Efficiency (%)
);

DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO solar_panel_battery_status (
            panel_id, 
            ts, 
            solar_irradiance, 
            ambient_temperature, 
            module_temperature, 
            wind_speed, 
            energy_output, 
            voltage, 
            current, 
            power_output, 
            state_of_charge, 
            inverter_efficiency
        ) VALUES (
            'SOLAR_PANEL' || LPAD(i::TEXT, 1, '0'), 
            CURRENT_TIMESTAMP - (random() * interval '30 day'), -- Timestamp
            200 + RANDOM() * 800,
            15 + RANDOM() * 25,
            20 + RANDOM() * 60,
            RANDOM() * 10,
            500 + RANDOM() * 4500,
            200 + RANDOM() * 400,
            1 + RANDOM() * 9,
            100 + RANDOM() * 900,
            5.0 + random() * 50.0, -- Random SOC between 5% and 100%
            85 + RANDOM() * 14
        );
    END LOOP;
END $$;