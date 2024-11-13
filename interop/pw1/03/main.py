import re
import csv
from collections import defaultdict

def count_admin1_codes(file_path):
    # Dictionary to store count of admin1 codes per country
    country_counts = defaultdict(int)
    
    # Regex to parse each line, extracting the country code (first 2 chars of code)
    pattern = re.compile(r'^([A-Z]{2})\.\w+')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                country_code = match.group(1)
                country_counts[country_code] += 1

    return country_counts

def get_country_names(file_path):
    country_names = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.split('\t')
            country_code = parts[0]
            country_name = parts[4]
            country_names[country_code] = country_name
    return country_names

def export_to_csv(data, country_names, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Country Code', 'Country Full Name', 'Number of Admin1 Regions'])

        for code, count in sorted(data.items()):
            full_name = country_names.get(code, "Unknown")
            csv_writer.writerow([code, full_name, count])

# File paths
admin1_file = '03/admin1CodesASCII.txt'
countries_files = '03/countryInfo.txt'
output_csv = '03/output.csv'

# Process the file and export the results
counts = count_admin1_codes(admin1_file)
country_names = get_country_names(countries_files)
export_to_csv(counts, country_names, output_csv)
print(f"Results saved in {output_csv}")
