#
# Analyze a CSV file of frequencies for intermod conflicts.
#

from ham_intermod.objects import Freq

def analyze(csv_string):
    """
    Analyze the list of frequencies in the CSV file for intermod
    conflicts.
    (NOT COMPLETED YET. For now, it just returns the CSV file contents)
    """
    analysis_report = ""
    channel_dict = csv2dict(csv_string)
    unique_freqs = channel_dict2list(channel_dict)
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
    report_out +="<h3><u>3rd Order Intermodulation Hits</u></h3>"
    report_out += "<table>"
    analysis_freqs = append_negs_to_list_of_nums(freqs.copy()) # copy pointer
    for i in range(0, len(freqs)): # Only loop through +ve nums
        for j in range(i, len(analysis_freqs)):
            for k in range(j, len(analysis_freqs)):
                f1, f2, f3 = analysis_freqs[i], analysis_freqs[j], analysis_freqs[k]
                if all_frequencies_kosher(f1, f2, f3):
                    intermod = f1 + f2 + f3
                    if intermod in freqs:
                        report_out += (f"<tr><td>{f1}</td>")
                        if f2 < 0: # If f2 < 0, then subtract abs(f2) in report
                            report_out += (f"<td><center>-</center></td> \
                                           <td>{abs(f2)}</td>")
                        else:      # else add f2
                            report_out += (f"<td><center>+</center></td> \
                                           <td>{f2}</td>")
                        if f3 < 0: # If f3 < 0, then subtract abs(f3) in report
                            report_out += (f"<td><center>-</center></td> \
                                            <td>{abs(f3)}</td><td>=</td> \
                                            <td>{intermod}</td></tr>")
                        else:       # else add f3
                            report_out += (f"<td><center>+</center></td> \
                                            <td>{f3}</td><td>=</td> \
                                            <td>{intermod}</td></tr>")
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
    report_out += "</table>"
    return(report_out)

def check_for_2nd_order_intermod(freqs, agg_score, vic_score):
    """
    Scan the list of frequencies for any 2nd order intermod hits and report
    the results.
    """
    report_out = "<h3><u>2nd Order Intermodulation Hits</u></h3>"
    report_out += "<table>"
    analysis_freqs = append_negs_to_list_of_nums(freqs.copy()) # copy pointer
    for i in range(0, len(freqs)): # Only loop through +ve nums
        for j in range(i, len(analysis_freqs)):
            f1, f2 = analysis_freqs[i], analysis_freqs[j]
            if (f2 > 0) or (f1 > f2 * -1): # Redundant when f2 < 0 and abs(f2) > f1
                intermod = f1 + f2
                if intermod in freqs:
                    report_out += (f"<tr><td>{f1}</td>")
                    if f2 < 0:  # If f2 < 0, then subtract abs(f2) in report
                        report_out += (f"<td><center>-</center></td> \
                                        <td>{abs(f2)}</td><td>=</td> \
                                        <td>{intermod}</td></tr>")
                    else:        # else add f2
                        report_out += (f"<td><center>+</center></td> \
                                        <td>{f2}</td><td>=</td> \
                                        <td>{intermod}</td></tr>")
                    vic_score[freqs.index(intermod)] += 1
                    agg_score[i] += 1
                    if (abs(f2) != abs(f1)): # Don't double-count when scoring
                        if j < len(freqs):
                            agg_score[j] += 1
                        else:
                            agg_score[len(analysis_freqs)-j-1] += 1
    report_out += "</table>"
    return(report_out)

def report_scores(report_out, freqs, agg_score, vic_score):
    """
    Report the total aggressor and victim scores
    """
    
    #
    # Report no intermod hits if there are no aggressors
    #
    report_out += (f"\n<h3><u>Hit Scores</u></h3>")
    if sum(agg_score) == 0:
        report_out += (f"No intermod hits found!\n")
        return(report_out)
    #
    # Else total the aggressor and victim scores for each frequency and sort
    # the list by total score.
    #
    freqs_unsorted = []
    freqs_sorted_by_tot_score = []
    report_out += "<table>"
    for i in range(0, len(freqs)):
        total_score = agg_score[i] + vic_score[i]
        freqs_unsorted.append(Freq(freqs[i], agg_score[i], vic_score[i], total_score))

    freqs_sorted_by_tot_score = sorted(freqs_unsorted, key=lambda x: x.total_score, reverse=True)

    for i in range(0, len(freqs_sorted_by_tot_score)):
        agg_percent = freqs_sorted_by_tot_score[i].aggressor_score / sum(agg_score) * 100
        vic_percent = freqs_sorted_by_tot_score[i].victim_score / sum(vic_score) * 100
        total_percent = freqs_sorted_by_tot_score[i].total_score / (sum(agg_score) + sum(vic_score)) * 100
        if freqs_sorted_by_tot_score[i].total_score > 0:     # Only print hit score if total_score > 0
            report_out += (f"<tr><td>{freqs_sorted_by_tot_score[i].frequency}:</td> \
                            <td>{freqs_sorted_by_tot_score[i].aggressor_score} aggressors ({round(agg_percent)}%),</td> \
                            <td>{freqs_sorted_by_tot_score[i].victim_score} victims ({round(vic_percent)}%),</td> \
                            <td>TOTAL SCORE=</td> \
                            <td align='right'>{freqs_sorted_by_tot_score[i].total_score} ({round(total_percent)}%)</td></tr>")
    report_out += "</table>"
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

def channel_dict2list(channel_dict):
    """
    Convert the CSV dictionary of radio channel information into a list of
    unique radio frequencies sorted in ascending order.
    """
    i=0
    all_freqs = []
    for rx_freq in channel_dict['RxFreq']:
        rx_freq = ''.join(rx_freq.split()) # Remove any whitespace
        offset = channel_dict['TxFreq'][i]
        offset = ''.join(offset.split()) # Remove any whitespace
        rx_freq_float = float(rx_freq)
        match offset:
            case "" | "S" | "s":
                tx_freq_float = rx_freq_float
            case "-":
                tx_freq_float = (rx_freq_float - 0.6) if (rx_freq_float <= 148) \
                    else (rx_freq_float - 5) 
            case "+":
                tx_freq_float = (rx_freq_float + 0.6) if (rx_freq_float <= 148) \
                    else (rx_freq_float + 5)
            case _ :
                tx_freq_float = float(offset)
        tx_freq_float = round(tx_freq_float, 3)
        all_freqs.append(rx_freq_float)
        all_freqs.append(tx_freq_float)
        i += 1
    unique_freqs = sorted(list(set(all_freqs)))
    return(unique_freqs)
