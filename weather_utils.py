"""
(°F – 32) x 5/9 = °C
"""
def convert_fahrenheit_to_celsius(fahrenheit_degrees):
    return ( fahrenheit_degrees - 32 ) * ( 5/9 )

"""
km = miles / 0.62137
"""
def convert_miles_to_km( mph ):
    return mph / 0.62137

degree_sign = u'\N{DEGREE SIGN}'
