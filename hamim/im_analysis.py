#
# Analyze a CSV file of frequencies for intermod conflicts.
#

def analyze(csv_string):
    """
    Analyze the list of frequencies in the CSV file for intermod
    conflicts.
    (NOT COMPLETED YET. For now, it just returns the CSV file contents)
    """
    analysis_report = ""
    channel_list = csv2dict(csv_string)
    unique_freqs_strings = set(channel_list['TxFreq'] + channel_list['RxFreq'])
    unique_freqs = [float(x) for x in unique_freqs_strings] # Convert to floats
    unique_freqs.sort(reverse=True)
    analysis_report += report_unique_freqs(unique_freqs)
    analysis_report += check_for_intermod(unique_freqs)
    return(analysis_report)

def report_unique_freqs(freq_list):
    """
    Report the list of unique frequencies found in the CSV file
    """
    report_out  = 'Unique frequencies\n'
    report_out += '------------------\n'
    for element in freq_list:
        report_out += (f"{element}\n")
    return(report_out)

def check_for_intermod(freqs):
    """
    Scan a list of frequencies to check for combinations that cause intermod
    conflicts
    """
    for freq in freqs:
        print(f"diagnostics {freq}")
    report_out = check_for_2nd_order_intermod(freqs)
    return(report_out)

def check_for_2nd_order_intermod(freqs):
    """
    Scan the list of frequencies for any 2nd order intermod hits and report
    the results.
    """
    report_out ="\n2nd Order Intermodulation\n"
    report_out+="-------------------------\n"
    analysis_freqs = append_negs_to_list_of_nums(freqs)
    for i in range(0, int(len(analysis_freqs)/2)):
        for j in range(i, len(analysis_freqs)):
            f1, f2 = analysis_freqs[i], analysis_freqs[j]
            if (f2 > 0) or (f1 > f2 * -1):
                intermod = f1 + f2
                report_out += (f"{f1} + {f2} = {intermod}")
                if intermod in freqs:
                    report_out += (f" HIT\n")
                else:
                    report_out += (f"\n")
    return(report_out)

def append_negs_to_list_of_nums(nums):
    """
    Copy all the values from a list, multiplies them by -1 and appends them to
    the end of the list.
    """
    for i in range(len(nums)-1, -1, -1):
        nums.append(nums[i] * -1)
    return(nums)

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