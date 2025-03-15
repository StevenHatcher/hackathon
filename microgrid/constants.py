# Constant values for calculations

SECONDS = 60
MINUTES = 60
HOURS = 24


# Source: https://apps.cer-rec.gc.ca/Conversion/conversion-tables.aspx
# Units in Joules (watt-seconds)
WATT = 1
GIGAJOULE = 1e9
KWH = WATT * SECONDS * MINUTES * 1000
GIGAJOULE_KWH = GIGAJOULE / KWH
# print(GIGAJOULE_KWH)

# Weight in KG
lb_to_kg = 0.453592

# solar panels
SOLAR_SPECS = {
    {"60 Cell": {"size": [3, 5.5], "energy KWH": 5.775, "weight": 40}},
    {"other": {"size": [1, 1], "energy KWH": 6, "weight": 30}},
}
