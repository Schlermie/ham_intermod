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
    report_out  = '<h3><u>Unique Frequencies</u></h3>'
    for element in freq_list:
        report_out += (f"{element}\n")
    return(report_out)

def check_for_intermod(freqs):
    """
    Scan a list of frequencies to check for combinations that cause intermod
    conflicts
    """
    # for freq in freqs:
    #     print(f"diagnostics {freq}")
    aggressor_score = [0] * len(freqs)
    victim_score = [0] * len(freqs)
    report_out = check_for_2nd_order_intermod(freqs, aggressor_score, victim_score)
    report_out = check_for_3rd_order_intermod(report_out, freqs, aggressor_score, victim_score)
    report_out = report_scores(report_out, freqs, aggressor_score, victim_score)
    return(report_out)

def all_frequencies_kosher(f1, f2, f3):
    """
    Function to check if all three frequencies are valid for 3rd order intermod
    analysis. Return True if valid. Return False if any of:
      1. f1, f2, and f3 contain two opposite values
      2. 
      3. 
    """
    neg_f1 = f1 * -1
    neg_f2 = f2 * -1
    if (neg_f1 == f2) or (neg_f1 == f3) or (neg_f2 == f3):
        return(False)
    return(True)

def check_for_3rd_order_intermod(report_out, freqs, agg_score, vic_score):
    """
    Scan the list of frequencies for any 3rd order intermod hits and report
    the results.
    """
    report_out +="\n<h3><u>3rd Order Intermodulation Hits</u></h3>"
    analysis_freqs = append_negs_to_list_of_nums(freqs.copy()) # copy pointer
    for i in range(0, len(freqs)): # Only loop through +ve nums
        for j in range(i, len(analysis_freqs)):
            for k in range(j, len(analysis_freqs)):
                f1, f2, f3 = analysis_freqs[i], analysis_freqs[j], analysis_freqs[k]
                if all_frequencies_kosher(f1, f2, f3):
                    intermod = f1 + f2 + f3
                    if intermod in freqs:
                        report_out += (f"{f1} ")
                        if f2 < 0: # If f2 < 0, then subtract abs(f2) in report
                            report_out += (f"- {abs(f2)} ")
                        else:
                            report_out += (f"+ {f2} ")
                        if f3 < 0: # If f3 < 0, then subtract abs(f3) in report
                            report_out += (f"- {abs(f3)} = {intermod}\n")
                        else:
                            report_out += (f"+ {f3} = {intermod}\n")
                        vic_score[freqs.index(intermod)] += 1
                        agg_score[i] += 1
                        if (abs(f2) != abs(f1)): # Don't double-count when scoring
                            if j < len(freqs):
                                agg_score[j] += 1
                            else:
                                agg_score[len(analysis_freqs)-j-1] += 1
                        if (abs(f3) != abs(f1)) and (abs(f3) != abs (f2)): # Don't double-count when scoring
                            if k < len(freqs):
                                agg_score[k] += 1
                            else:
                                agg_score[len(analysis_freqs)-k-1] += 1
    return(report_out)

def check_for_2nd_order_intermod(freqs, agg_score, vic_score):
    """
    Scan the list of frequencies for any 2nd order intermod hits and report
    the results.
    """
    report_out ="\n<h3><u>2nd Order Intermodulation Hits</u></h3>"
    analysis_freqs = append_negs_to_list_of_nums(freqs.copy()) # copy pointer
    for i in range(0, len(freqs)): # Only loop through +ve nums
        for j in range(i, len(analysis_freqs)):
            f1, f2 = analysis_freqs[i], analysis_freqs[j]
            if (f2 > 0) or (f1 > f2 * -1): # Redundant when f2 < 0 and abs(f2) > f1
                intermod = f1 + f2
                if intermod in freqs:
                    report_out += (f"{f1} ")
                    if f2 < 0:  # If f2 < 0, then subtract abs(f2) in report
                        report_out += (f"- {abs(f2)} = {intermod}\n")
                    else:
                        report_out += (f"+ {f2} = {intermod}\n")
                    vic_score[freqs.index(intermod)] += 1
                    agg_score[i] += 1
                    if (abs(f2) != abs(f1)): # Don't double-count when scoring
                        if j < len(freqs):
                            agg_score[j] += 1
                        else:
                            agg_score[len(analysis_freqs)-j-1] += 1
    return(report_out)

def report_scores(report_out, freqs, agg_score, vic_score):
    """
    Report the total aggressor and victim scores
    """
    report_out += (f"\n<h3><u>Hit Scores</u></h3>")
    if sum(agg_score) == 0:
        report_out += (f"No intermod hits found!\n")
        return(report_out)
    for i in range(0, len(freqs)):
        total_score = agg_score[i] + vic_score[i]
        agg_percent = agg_score[i] / sum(agg_score) * 100
        vic_percent = vic_score[i] / sum(vic_score) * 100
        total_percent = total_score / (sum(agg_score) + sum(vic_score)) * 100
        if total_score > 0:     # Only print hit score if total_score > 0
            report_out += (f"{freqs[i]}: \
                            {agg_score[i]} aggressors ({round(agg_percent)}%), \
                            {vic_score[i]} victims ({round(vic_percent)}%), \
                            TOTAL SCORE={total_score} ({round(total_percent)}%)\n")
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