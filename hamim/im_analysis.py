#
# Analyze a CSV file of frequencies for intermod conflicts.
#

from hamim.objects import Freq

def analyze(csv_string):
    """
    Analyze the list of frequencies in the CSV file for intermod
    conflicts.
    """
    analysis_report = ""
    channel_dict = csv2dict(csv_string)
    list_of_unique_freq_lists, channel_label_dict = channel_dict_to_list_of_freqlists(channel_dict)
    for unique_freq_list in list_of_unique_freq_lists:
        analysis_report += report_unique_freqs(unique_freq_list, channel_label_dict)
        analysis_report += check_for_intermod(unique_freq_list, channel_label_dict)
    return(analysis_report)

def report_unique_freqs(freq_list, frequency_label_dict):
    """
    Report the list of unique frequencies found in the CSV file. Include a
    label for each frequency listed, based on the labels found in the CSV file.
    """
    report_out  = '<h3><u>Unique Frequencies</u></h3>'
    report_out += '<table>'
    print (freq_list)
    for element in freq_list:
        report_out += (f"<tr><td><b>{element}:</b></td> \
                         <td>{frequency_label_dict[element]}</td></tr>")
    report_out += '</table>'
    return(report_out)

def check_for_intermod(freqs, frequency_label_dict):
    """
    Scan a list of frequencies to check for combinations that cause intermod
    conflicts
    """
    aggressor_score = [0] * len(freqs)
    victim_score = [0] * len(freqs)
    report_out = check_for_2nd_order_intermod(freqs, aggressor_score, victim_score)
    report_out = check_for_3rd_order_intermod(report_out, freqs, aggressor_score, victim_score)
    report_out = report_scores(report_out, freqs, aggressor_score, victim_score, frequency_label_dict)
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
    report_out = "\n<h3><u>2nd Order Intermodulation Hits</u></h3>"
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

def report_scores(report_out, freqs, agg_score, vic_score, frequency_label_dict):
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
            report_out += (f"<tr><td><b>{freqs_sorted_by_tot_score[i].frequency}</b></td> \
                            <td><b>({frequency_label_dict[freqs_sorted_by_tot_score[i].frequency]}):</b></td> \
                            <td>{freqs_sorted_by_tot_score[i].aggressor_score} aggressors ({round(agg_percent)}%),</td> \
                            <td>{freqs_sorted_by_tot_score[i].victim_score} victims ({round(vic_percent)}%),</td> \
                            <td>TOTAL SCORE=</td> \
                            <td align='right'>{freqs_sorted_by_tot_score[i].total_score} ({round(total_percent)}%)</td></tr>")
    report_out += '</table><hr style="height:6px;background-color:#333;">'
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

def channel_dict_to_list_of_freqlists(channel_dict):
    """
    Convert the CSV dictionary of radio channel information into a list of lists
    of unique radio frequencies sorted in ascending order. Multiple lists are
    created to account for all combinations of backup frequencies.

    Return a list of frequency lists and also a dictionary that assigns a label
    to each frequency.
    """
    if 'Backups' in channel_dict.keys(): # If CSV has Backups column, process backups
        list_of_channel_dicts = create_list_of_channel_dicts(channel_dict)
    else:
        list_of_channel_dicts = []
        list_of_channel_dicts.append(channel_dict)
    list_of_freq_lists = []
    channel_label_dict = {}
    for channel_dict in list_of_channel_dicts:
        all_freqs = []
        i=0
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
            if 'Label' in channel_dict.keys(): # Create dictionary of labels for each frequency
                channel_label_dict[rx_freq_float] = channel_dict['Label'][i]
                channel_label_dict[tx_freq_float] = channel_dict['Label'][i]
            else:
                channel_label_dict[rx_freq_float] = ""
                channel_label_dict[tx_freq_float] = ""
            i += 1
        unique_freqs = sorted(list(set(all_freqs))) # Create list of frequencies
        list_of_freq_lists.append(unique_freqs) # Create list of frequency lists
    return(list_of_freq_lists, channel_label_dict)

def create_list_of_channel_dicts(channel_dict):
    """
    Read a raw list of channels converted from the user CSV file. Convert that
    list of channels to a list of channel lists by removing all but one backup
    frequency found in the Backups list. If there is more than one type of
    backup frequency, then build lists for all combinations of backup frequency
    types.
    """
    channel_dict_keys = channel_dict.keys()
    backup_keys = set(channel_dict['Backups']) # Read list of backup keys from csv
    backup_keys.remove('') # Remove empty string from list of backup keys
    channel_dict_backups = initialize_dict_of_dicts_of_lists(backup_keys, channel_dict_keys)
    channel_dict_no_backups = initialize_dict_of_lists(channel_dict_keys)

    #
    # Copy backup channels to channel_dict_backups
    # Copy non-backup channels to channel_dict_no_backups
    #
    for i, backup_tag in enumerate(channel_dict['Backups']):
        for key in channel_dict_keys: # Separate channels to backup or no backup
            if backup_tag:
                channel_dict_backups[backup_tag][key].append(channel_dict[key][i])
            else:
                channel_dict_no_backups[key].append(channel_dict[key][i])
    # list_of_backup_channel_lists = list(channel_dict_backups.values())
    list_of_backup_channel_lists = channel_dict_backups_to_list_of_backup_channel_lists(channel_dict_backups)
    list_of_backup_combos = generate_backup_combos(list_of_backup_channel_lists)
    list_of_channels_without_backups = dict_of_lists_to_list_of_strings(channel_dict_no_backups)
    all_combos_of_channel_lists_w_and_wo_backups = make_all_combo_list_w_and_wo_backups(list_of_backup_combos, list_of_channels_without_backups)

    # Convert the list of channel rows back to dictionary format with CSV
    # headers used as keys for each CSV column.
    list_of_channel_dict_combos = []
    for channel_list in all_combos_of_channel_lists_w_and_wo_backups:
        channel_dict_one_backup_combo = channel_list_to_channel_dict(channel_list, channel_dict_keys)
        list_of_channel_dict_combos.append(channel_dict_one_backup_combo)

    return (list_of_channel_dict_combos)
    # return(False)

def channel_list_to_channel_dict(channel_list, channel_dict_keys):
    """
    Convert a list of channels from rows back to dictionary format with CSV
    headers used as keys for each CSV column.

    Args:
        channel_list(list): List of channels with channel information delimited
            by commas
        channel_dict_keys(list): List of all the column headers from the CSV file

    Returns:
        channel_dict(dictionary of lists): A dictionary of channel information
            for a list of channels, where the keys are defined by
            channel_dict_keys and the values are lists of channel information.
    """
    delimiter = ","
    channel_dict = initialize_dict_of_lists(channel_dict_keys)
    channel_dict_keys_list = list(channel_dict_keys)
    for channel in channel_list:
        channel_data = channel.split(delimiter)
        for i, value in enumerate(channel_data):
            channel_dict[channel_dict_keys_list[i]].append(value)
    return(channel_dict)

def make_all_combo_list_w_and_wo_backups(backup_channel_lists, chs_wo_backups):
    """
    Combine the backup channel combinations with the list of channels that
    don't contain backups to create all channel lists that consider all legal
    combinations of backup channels.

    Args:
        backup_channel_lists(list of lists): Lists of all legal combinations
                                             of backup channel possibilities
        chs_wo_backups(list): Lists of all the channels that aren't backups

    Returns:
        list_of_combined_lists(list of lists): A list of lists of all possible
                    backup channel combinations combined with the list of
                    channels that do not have backup channels. 
    """
    list_of_combined_lists = []
    for backup_channel_combo in backup_channel_lists:
        combined_list = backup_channel_combo + chs_wo_backups
        list_of_combined_lists.append(combined_list)
    return(list_of_combined_lists)


def channel_dict_backups_to_list_of_backup_channel_lists(dict_of_dicts_of_lists):
    """
    Convert a dictionary of dictionaries of lists to a list of lists where the
    inner list is formed by concatenating elements from each list across
    the inner dictionaries. The outer list (corresponding to the keys of the outer
    dictionary) is just a list of those lists.

    Args:
        dict_of_dicts_of_lists: A dictionary of dictionaries of lists

    Returns:
        list_of_lists_of_strings: A list of lists of strings
    """
    list_of_dicts_of_lists = list(dict_of_dicts_of_lists.values())
    list_of_lists_of_strings = []
    for dict_of_lists in list_of_dicts_of_lists: # Transform dicts of lists to list of lists of strings made
                                                 # by concatenating elements from each column to create a row.
        list_of_strings = dict_of_lists_to_list_of_strings(dict_of_lists)  
        list_of_lists_of_strings.append(list_of_strings)
    return(list_of_lists_of_strings)

def dict_of_lists_to_list_of_strings(dict_of_lists):
    """
    Convert a dictionary of lists to a list of strings where the
    strings are formed by concatenating elements from each list across
    the dictionaries.

    Args:
        dict_of_lists: A dictionaries of lists

    Returns:
        list_of_strings: A list of strings of contatenated items from the
                         dictionary lists.
    """
    delimiter = ","
    i=0
    list_of_strings = []
    first_key = next(iter(dict_of_lists))
    while i < len(dict_of_lists[first_key]):
        string = ""
        for dict_key in dict_of_lists.keys():
            string += f"{dict_of_lists[dict_key][i]}{delimiter}"
        string = string[:(len(delimiter) * -1)] # Remove final delimiter string
        list_of_strings.append(string)
        i += 1
    return (list_of_strings)


def initialize_dict_of_lists(dict_keys):
    """
    Initialize a dictionary of lists, given a list of keys to the dictionary.

    Args:
        dict_keys (list): A list of keys for the dictionary

    Returns:
        dict_of_lists = An initialized dictionary of lists
    """
    dict_of_lists = {}
    for key in dict_keys:
        dict_of_lists[key] = []
    return(dict_of_lists)

def initialize_dict_of_dicts_of_lists(outer_dict_keys, inner_dict_keys):
    """
    Initialize a dictionary of dictionaries of lists, given lists of keys to the
    outer and inner dictionaries.

    Args:
        outer_dict_keys (list): A list of keys for the outer dictionary
        inner_dict_keys (list): A list of keys for the inner dictionary

    Returns:
        dict_of_dicts_of_lists: An initializedd dictionary of dictionaries of lists
    """
    dict_of_dicts_of_lists = {}
    for outer_dict_key in outer_dict_keys:
        dict_of_dicts_of_lists[outer_dict_key] = {}
        for inner_dict_key in inner_dict_keys:
            dict_of_dicts_of_lists[outer_dict_key][inner_dict_key] = []
    return(dict_of_dicts_of_lists)

def initialize_list_of_dicts_of_lists(dict_keys):
    """
    Initialize a list of dictionaries of lists, given a list of keys to the
    dictionary.

    Args:
        dict_keys (list): A list of keys for the dictionary

    Returns:
        list_of_dicts_of_lists: An initializedd list of dictionaries of lists
    """
    list_of_dicts_of_lists = []
    dict_of_lists = {}
    for dict_key in dict_keys:
        dict_of_lists[dict_key] = []
    list_of_dicts_of_lists.append(dict_of_lists)
    return(list_of_dicts_of_lists)

def generate_backup_combos(lists_of_backup_channel_lists):
    """
    A recursive function that generates combinations of backup channels from N
    variable length lists of backup channels.

    Args:
        lists_of_backup_channel_lists (list of lists of channel strings)

    Returns:
        result (list of lists of combinations of channel strings)
    """
    if not lists_of_backup_channel_lists:
        return [[]]
    
    result = []
    for i in range(len(lists_of_backup_channel_lists[0])):
        for rest_of_the_outer_list in generate_backup_combos(lists_of_backup_channel_lists[1:]):
            result.append([lists_of_backup_channel_lists[0][i]] + rest_of_the_outer_list)

    return result