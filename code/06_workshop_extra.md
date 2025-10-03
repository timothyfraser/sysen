# Codebook for `onsen.csv`

| Variable | Type         | Description                                                                 | Example Values         |
|----------|--------------|-----------------------------------------------------------------------------|------------------------|
| id       | numeric (dbl)| Unique identifier for each observation (row).                              | 1, 2, 3, 4, 5          |
| time     | numeric (dbl)| Time index for the observation (likely measurement round or sampling time). | 1, 1, 1, 1, 1          |
| temp     | numeric (dbl)| Water temperature in degrees Celsius.                                       | 43.2, 45.3, 45.5, 43.9 |
| ph       | numeric (dbl)| Acidity/alkalinity of the water, measured on the pH scale (0–14).           | 5.1, 4.8, 6.2, 6.4     |
| sulfur   | numeric (dbl)| Sulfur concentration in the water (units not specified).                    | 0.0, 0.4, 0.9, 0.2     |
