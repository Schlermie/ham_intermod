#
# Analyze a CSV file of frequencies for intermod conflicts.
#

def analyze(csv_string):
    """
    Analyze the list of frequencies in the CSV file for intermod
    conflicts.
    (NOT COMPLETED YET. For now, it just returns the CSV file contents)
    """
    channel_list = csv2dict(csv_string)
    unique_freqs = set(channel_list['TxFreq'] + channel_list['RxFreq'])
    intermod_report = check_for_intermod(unique_freqs)
    return(unique_freqs)

def check_for_intermod(freqs):
    """
    Scan a list of frequencies to check for combinations that cause intermod
    conflicts
    """
    for freq in freqs:
        print(f"diagnostics {freq}")

    return(freqs)

def csv2dict(csv_string):
    """
    Convert a CSV file in the form of a string to a dictionary of lists
    """
    data_dict = {}

    # Convert the CSV string to a list of rows
    csv_rows = csv_string.splitlines()

    # Use the first row as column headers
    headers = csv_rows[0].split(',')
    num_columns = len(headers)

    # Initialize lists for each column in the dictionary
    for header in headers:
        data_dict[header] = []

    # Iterate over the remaining rows and populate the dictionary
    for row in csv_rows[1:]:
        row_data = row.split(',')
        if len(row_data) == num_columns:
            for i, header in enumerate(headers):
                data_dict[header].append(row_data[i])

    return data_dict