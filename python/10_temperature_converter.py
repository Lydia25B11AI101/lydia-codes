# Python Program 10: Temperature Converter
# Author: Lydia S. Makiwa
# Description: Converts between Celsius, Fahrenheit, and Kelvin

def celsius_to_fahrenheit(c): return (c * 9/5) + 32
def celsius_to_kelvin(c):     return c + 273.15
def fahrenheit_to_celsius(f): return (f - 32) * 5/9
def fahrenheit_to_kelvin(f):  return fahrenheit_to_celsius(f) + 273.15
def kelvin_to_celsius(k):     return k - 273.15
def kelvin_to_fahrenheit(k):  return celsius_to_fahrenheit(kelvin_to_celsius(k))

def convert(value, unit):
    unit = unit.upper()
    if unit == 'C':
        print(f"{value}°C = {celsius_to_fahrenheit(value):.2f}°F = {celsius_to_kelvin(value):.2f}K")
    elif unit == 'F':
        print(f"{value}°F = {fahrenheit_to_celsius(value):.2f}°C = {fahrenheit_to_kelvin(value):.2f}K")
    elif unit == 'K':
        print(f"{value}K  = {kelvin_to_celsius(value):.2f}°C = {kelvin_to_fahrenheit(value):.2f}°F")
    else:
        print("Invalid unit. Use C, F, or K.")

print("=== Temperature Converter ===")
print("Common temperatures:\n")
for val, unit in [(0,'C'), (100,'C'), (37,'C'), (32,'F'), (212,'F'), (0,'K')]:
    convert(val, unit)
