from geographiclib.geodesic import Geodesic

# Circuits List (Name, Latitude, Longitude, Continent, RaceDate)
circuits = [
    ("Melbourne Grand Prix Circuit", -37.8497, 144.968, "Oceania", "2025-03-16"),
    ("Shanghai International Circuit", 31.3389, 121.2189, "Asia", "2025-03-23"),
    ("Suzuka International Racing Course", 34.8431, 136.5419, "Asia", "2025-04-06"),
    ("Bahrain International Circuit", 26.0325, 50.5106, "Asia", "2025-04-13"),
    ("Jeddah Corniche Circuit", 21.6319, 39.1044, "Asia", "2025-04-20"),
    ("Miami International Autodrome", 25.9581, -80.2389, "North America", "2025-05-04"),
    ("Autodromo Enzo e Dino Ferrari (Imola)", 44.3439, 11.7167, "Europe", "2025-05-18"),
    ("Circuit de Monaco", 43.7347, 7.4206, "Europe", "2025-05-25"),
    ("Circuit de Barcelona-Catalunya", 41.57, 2.2611, "Europe", "2025-06-01"),
    ("Circuit Gilles-Villeneuve", 45.5000, -73.5228, "North America", "2025-06-15"),
    ("Red Bull Ring", 47.2196, 14.7646, "Europe", "2025-06-29"),
    ("Silverstone Circuit", 52.0786, -1.0169, "Europe", "2025-07-06"),
    ("Circuit de Spa-Francorchamps", 50.4372, 5.9714, "Europe", "2025-07-27"),
    ("Hungaroring", 47.5822, 19.2511, "Europe", "2025-08-03"),
    ("Circuit Zandvoort", 52.3889, 4.5409, "Europe", "2025-08-31"),
    ("Autodromo Nazionale Monza", 45.6156, 9.2811, "Europe", "2025-09-07"),
    ("Baku City Circuit", 40.3725, 49.8533, "Asia", "2025-09-21"),
    ("Marina Bay Street Circuit", 1.2914, 103.8640, "Asia", "2025-10-05"),
    ("Circuit of the Americas", 30.1328, -97.6411, "North America", "2025-10-19"),
    ("Autodromo Hermanos Rodriguez", 19.4042, -99.0907, "North America", "2025-10-26"),
    ("Autodromo Jose Carlos Pace (Interlagos)", -23.7036, -46.6997, "South America", "2025-11-09"),
    ("Las Vegas Strip Circuit", 36.1147, -115.1728, "North America", "2025-11-23"),
    ("Lusail International Circuit", 25.4892, 51.4531, "Asia", "2025-11-30"),
    ("Yas Marina Circuit", 24.4672, 54.6031, "Asia", "2025-12-08")
]

# Initialize circuit dictionary
circuit_dict = {}

for i, (name, lat, lon, continent, race_date) in enumerate(circuits):
    circuit_dict[name] = {
        "Latitude": lat,
        "Longitude": lon,
        "Continent": continent,
        "RaceDate": race_date
    }

if __name__ == "__main__":
    # if you want to print the created circuit dictionary
    print(circuit_dict)
