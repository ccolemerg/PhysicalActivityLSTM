class DataProcessing:
	
	 def __init__(self, file_name):
            self.file_name = file_name
            

	def print_activity_table(day,activity_table, activity_table_minutes):
	    print(day + ";" + activity_table['Still'] + ';' + activity_table['Tilting'] + ';' + activity_table['Walking'] + ';'+
		activity_table['Running'] + ';' + activity_table['In a vehicle'] + ';' + activity_table['On a bicycle'] + '\n')

	    print(day + ";" + str(activity_table_minutes['Still']) + ';' + str( activity_table_minutes['Tilting']) + ';' + 	    str(activity_table_minutes['Walking']) + ';' +str(activity_table_minutes['Running']) + ';' + str(
		activity_table_minutes['In a vehicle']) + ';' + str(activity_table_minutes['On a bicycle']) + '\n')


	def days_of_logger():
	    all_days = []

	    with open('PhysicalActivity.txt', 'r') as reader:
		for line in reader:
		    line_arr = line.split(';')
		    if not line.startswith('[D'):
		        print(line_arr[0])
		        if line_arr[0] not in all_days and len(line_arr[0]) == 10:
		            all_days.append(line_arr[0])

	    print(all_days)

	    with open('Daily_statistic.txt', 'w') as writer:
		writer.write('Date;Still;Tilting;Walking;Running;In a vehicle;On a bicycle' + '\n')
		activity_table = {"Still": "00:00:00", "Tilting": "00:00:00", "Walking": "00:00:00", "Running": "00:00:00",
		                  "In a vehicle": "00:00:00",
		                  "On a bicycle": "00:00:00"}
		activity_table_minutes = {"Still": 0, "Tilting": 0, "Walking": 0, "Running": 0, "In a vehicle": 0,
		                          "On a bicycle": 0}

		for day in all_days:
		    print(day)
		    daily_data = create_data_daily(day)
		    daily_data_arr = str(daily_data)[1:-1].split(',')
		    for d_data in daily_data_arr:
		        d_data_arr = d_data.split("'")
		        activity_table[str(d_data_arr[1])] = d_data_arr[3]
		        activity_table_minutes[d_data_arr[1]] = time_convert_to_minutes(d_data_arr[3])

		    writer.write(day+";"+activity_table['Still']+';'+activity_table['Tilting']+';'+activity_table['Walking']+';'+
		                  activity_table['Running']+';'+activity_table['In a vehicle']+';'+activity_table['On a bicycle' +'\n')

		    writer.write(day + ";" + str(activity_table_minutes['Still']) + ';' + str(
		        activity_table_minutes['Tilting']) + ';' + str(activity_table_minutes['Walking']) + ';' +
		                 str(activity_table_minutes['Running']) + ';' + str(
		        activity_table_minutes['In a vehicle']) + ';' + str(activity_table_minutes['On a bicycle']) + '\n')

		    activity_table = {"Still": "00:00:00", "Tilting": "00:00:00", "Walking": "00:00:00", "Running": "00:00:00",
		                      "In a vehicle": "00:00:00", "On a bicycle": "00:00:00"}
		    activity_table_minutes = {"Still": 0, "Tilting": 0, "Walking": 0, "Running": 0, "In a vehicle": 0,
		                              "On a bicycle": 0}


	def activity_tables_for_24hours(file_name, day):
	    activity_table = {}

	    with open(self.file_name, 'r') as reader:
		for line in reader:
		    # print(line)
		    line_arr = line.split(';')
		    convert_arr = str(line_arr[2])[1:-1]
		    convert_arr_sp = convert_arr.split(',')
		    temp_table = {}

		    for con in convert_arr_sp:
		        con_arr = con.split("'")
		        temp_table[con_arr[1]] = con_arr[3]

		    activity_table[line_arr[0]+';'+line_arr[1]] = str(temp_table)


	    sum_same_activity = ['00:00:00', '00:00:00']
	    agg_activity_table = {"Still": "00:00:00", "Tilting": "00:00:00", "Walking": "00:00:00", "Running": "00:00:00",
		                      "In a vehicle": "00:00:00", "On a bicycle": "00:00:00"}

	    agg_activity_table_minutes = {"Still": 0, "Tilting": 0, "Walking": 0, "Running": 0, "In a vehicle": 0,
		                      "On a bicycle": 0}

	    for activity in activity_table:
		activity_arr_all = str(activity_table[activity]).split(",")
		for activity_item in activity_arr_all :
		    activity_arr =str(activity_item).split("'")
		    activity_name = activity_arr[1]
		    prev_time = agg_activity_table[activity_name]
		    if prev_time == "00:00:00":
		        agg_activity_table[activity_name] = activity_arr[3]
		    else:
		        sum_same_activity[1] = str(agg_activity_table[activity_name])
		        sum_same_activity[0] = str(activity_arr[3])
		        agg_activity_table[activity_name] = time_summation(sum_same_activity)


	    for agg in agg_activity_table:
		agg_minutes = time_convert_to_minutes(str(agg_activity_table[agg]))
		agg_activity_table_minutes[agg] = agg_minutes

	    print('aggregate : ')
	    agg_minutes, agg_total = total_time_activity_tables(agg_activity_table)
	    print(agg_activity_table)
	    print(agg_minutes)
	    print(agg_total)
	    print(agg_activity_table_minutes)

	    print_activity_table(day, agg_activity_table, agg_activity_table_minutes)


	def time_convert_to_minutes(time):
	    total = 0
	    h, m, s = map(int, time.split(":"))
	    #total += 3600 * h + 60 * m + s
	    total += 60 * h + 1 * m
	    return total


	def time_summation(time_arr):
	    total = 0
	    for time in time_arr:
		h, m, s = map(int, time.split(":"))
		total += 3600 * h + 60 * m + s
	    time_sum = "%02d:%02d:%02d" % (total / 3600, total / 60 % 60, total % 60)

	    return time_sum


	def total_time_activity_tables(activity_table):
	    table_time_arr = []
	    for activity in activity_table:
		table_time_arr.append(activity_table[activity])

	    total_time = time_summation(table_time_arr)
	    t = total_time.split(":")
	    total_minutes = int(t[0]) * 60 + int(t[1]) * 1 + int(t[2]) / 60

	    return int(total_minutes), total_time

	def time_comparison(s1,s2):
	    total_s1 = 0
	    h, m, s = map(int, str(s1).split(":"))
	    total_s1 += 3600 * h + 60 * m + s

	    total_s2 = 0
	    h, m, s = map(int, str(s2).split(":"))
	    total_s2 += 3600 * h + 60 * m + s

	    if total_s1 > total_s2:
		return True
	    else:
		return False


	def compare_hour_activity(activity_table):
	    total_minutes, total_time = total_time_activity_tables(activity_table)
	    print(int(total_minutes))

	    FMT = '%H:%M:%S'

	    missing_time = '00:00:00'

	    if total_minutes > 0:
		s2 = '00:59:00'
		s2_date = datetime.datetime.strptime(s2, FMT)

		time_diff = None
		total_time = datetime.datetime.strptime(total_time, FMT)

		time_diff = total_time - s2_date
		missing_time = s2_date - total_time

	    else:
		time_diff = datetime.datetime.strptime('00:00:00', FMT)



	    if int(total_minutes) < 59:
		return True, time_diff, total_minutes, missing_time
	    else:
		return False, time_diff,total_minutes, missing_time


	def create_data_daily(day:str):
	    prev_date = datetime.datetime.strptime(day + ' 00:00:00', '%d-%m-%Y %H:%M:%S')
	    activity_table = {}
	    sum_date = ['00:00:00', '00:00:00']

	    next_date = datetime.datetime.strptime(day, '%d-%m-%Y') + datetime.timedelta(days=1)
	    next_date = next_date.__str__().split(' ')[0]
	    next_date_arr = next_date.split('-')
	    r_next_date = next_date_arr[2] + '-' + next_date_arr[1] + '-' + next_date_arr[0]

	    with open('PhysicalActivity.txt', 'r') as reader:
		for line in reader:
		    # print(line)
		    line_arr = line.split(';')
		    most_detected_activity = 'None'
		    if len(line_arr) > 2:
		        activity_arr = line_arr[2].split(':')
		        if activity_arr[0] == 'On foot':
		            most_detected_activity = line_arr[3].split(':')[0]
		        else:
		            most_detected_activity = activity_arr[0]

		    if line_arr[0] == day and most_detected_activity != 'Unknown activity' and not line_arr[2].startswith(
		            'Field') and int(activity_arr[1]) > 80:

		        if most_detected_activity not in activity_table:
		            activity_table[most_detected_activity] = '00:00:00'

		        current_date = datetime.datetime.strptime(line_arr[0] + " " + line_arr[1], '%d-%m-%Y %H:%M:%S')
		        time_diff = current_date - prev_date
		        prev_date = current_date
		        sum_date[1] = time_diff.__str__()
		        sum_date[0] = activity_table[most_detected_activity]
		        activity_table[most_detected_activity] = time_summation(sum_date)

		    if next_date == line_arr[0] or r_next_date == line_arr[0]:
		        if not line_arr[2].startswith('Field') and not line.startswith(
		                '[D') and most_detected_activity != 'Unknown activity':
		            current_date = datetime.datetime.strptime(day + " 23:59:59", '%d-%m-%Y %H:%M:%S')
		            time_diff = current_date - prev_date
		            sum_date[1] = time_diff.__str__()
		            sum_date[0] = activity_table[most_detected_activity]
		            activity_table[most_detected_activity] = time_summation(sum_date)
		            break

	    return activity_table


	def is_greater_than_one_minutes(activity_table):
	    total_minutes, total_time = total_time_activity_tables(activity_table)

	    if int(total_minutes) > 0:
		return True
	    else:
		return False


	def time_difference(s1, s2):

	    s1_minutes = time_convert_to_minutes(s1)
	    s2_minutes = time_convert_to_minutes(s2)
	    FMT = '%H:%M:%S'
	    s1_date = datetime.datetime.strptime(s1, FMT)
	    s2_date = datetime.datetime.strptime(s2, FMT)

	    if s1_minutes > s2_minutes:
		time_diff = s1_date - s2_date
	    else:
		time_diff = s2_date - s1_date

	    return time_diff


	def create_data_hourly(day:str):
	    prev_date = datetime.datetime.strptime(day + ' 00:00:00', '%d-%m-%Y %H:%M:%S')
	    activity_table = {}
	    prev_activity_table = {}
	    exceed_prev_date = prev_date

	    all_hours_activity = {}

	    prev_activity_small =False

	    sum_date = ['00:00:00', '00:00:00']

	    prev_hour: int = 0
	    current_hour: int = 0
	    smaller_than = False
	    check_first_activity = False
	    diff_between_hour = 0

	    time_diff_update = False

	    FMT = '%H:%M:%S'
	    prev_missing_time = '00:00:00'


	    with open(self.file_name, 'r') as reader, open(self.file_name, 'w') as writer:
		for line in reader:
		    # print(line)
		    line_arr = line.split(';')
		    most_detected_activity = 'None'
		    if len(line_arr) > 2:
		        activity_arr = line_arr[2].split(':')
		        if activity_arr[0] == 'On foot':
		            most_detected_activity = line_arr[3].split(':')[0]
		        else:
		            most_detected_activity = activity_arr[0]

		    if line_arr[0] == day and most_detected_activity != 'Unknown activity' and not line_arr[
		        2].startswith(
		            'Field') and int(activity_arr[1]) > 80:

		        if len(line_arr) > 2:
		            time_arr = line_arr[1].split(":")
		            #   print(int(time_arr[0]))
		            current_hour = int(time_arr[0])

		        total_time_table = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
		        exceed_time = False

		        if current_hour != prev_hour:
		            diff_between_hour = current_hour - prev_hour

		            if diff_between_hour > 1:
		                exceed_prev_date = datetime.datetime.strptime(line_arr[0] + " " + line_arr[1],'%d-%m-%Y %H:%M:%S')
		                rr, tt = total_time_activity_tables(prev_activity_table)

		                for i in range(diff_between_hour - 1):
		                    missing_hour = current_hour - diff_between_hour + i + 1
		                    datetimeFormat = '%d-%m-%Y %H:%M:%S'
		                    date1 = line_arr[0] + ' ' + line_arr[1]
		                    missing_hour = line_arr[0] + ' 0' + str(missing_hour) + ':00:00'

		                    if is_greater_than_one_minutes(activity_table) and i == 0:
		                        total_minutes, total_time = total_time_activity_tables(activity_table)
		                        next_hour_diff = time_difference('01:00:00', total_time)
		                        activity_table[most_detected_activity] = str(next_hour_diff)
		                    else:
		                        activity_table[most_detected_activity] = '01:00:00'

		                    missing_hour_arr = missing_hour.__str__().split(' ')
		                    writer.write(missing_hour_arr[0]+';'+missing_hour_arr[1]+ ";" + activity_table.__str__() + "\n")
		                    all_hours_activity[missing_hour_arr[0]+';'+missing_hour_arr[1]]=activity_table
		                    # activity_table = {}
		                    date2 = line_arr[0] + ' 01:00:00'
		                    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2,
		                                                                                                          datetimeFormat)

		                    if is_greater_than_one_minutes(activity_table) and i ==0 :
		                        activity_table = {}

		            prev_hour = current_hour
		            prev_activity_table = activity_table
		            smaller_than, total_time_table,total_minutes, missing_time = compare_hour_activity(prev_activity_table)
		            check_first_activity = True
		            if smaller_than and total_minutes >= 57 :
		                print(activity_table)
		                writer.write(line_arr[0] + ";" + line_arr[1] + ";" + activity_table.__str__() + "\n")
		                all_hours_activity[line_arr[0] + ";" + line_arr[1]] = activity_table
		                activity_table = {}
		                prev_activity_table = {}
		            elif smaller_than and total_minutes < 57 :
		                prev_activity_small = True


		        if most_detected_activity not in activity_table:
		            activity_table[most_detected_activity] = '00:00:00'

		        current_date = datetime.datetime.strptime(line_arr[0] + " " + line_arr[1], '%d-%m-%Y %H:%M:%S')

		        time_diff = current_date - prev_date

		        if diff_between_hour > 1:
		            prev_date = exceed_prev_date
		            diff_between_hour = 0
		        else:
		            prev_date = current_date
		        # print(time_diff)

		        if not smaller_than and check_first_activity == True:
		            check_first_activity = False
		            exceed_time = True
		            sum_date[1] = total_time_table.__str__()
		            sum_date[0] = prev_activity_table[most_detected_activity]
		            time_summation_result =  time_summation(sum_date)
		            prev_activity_table[most_detected_activity] = time_summation_result
		            if time_comparison(str(time_summation_result), str(prev_missing_time)):
		                time_summation_result = time_difference(str(time_summation_result), str(prev_missing_time))
		                prev_activity_table[most_detected_activity] = str(time_summation_result)
		                prev_missing_time ='00:00:00'

		            prev_date_arr = prev_date.__str__().split(' ')
		            prev_date_rev_arr = prev_date_arr[0].split('-')
		            prev_date_revert = prev_date_rev_arr[2]+'-'+prev_date_rev_arr[1]+'-'+prev_date_rev_arr[0]
		            writer.write(prev_date_revert +";" + prev_date_arr[1] + ";" + prev_activity_table.__str__() + "\n")
		            all_hours_activity[prev_date_revert +";" + prev_date_arr[1]] = prev_activity_table
		            prev_activity_table = {}


		        if smaller_than and prev_activity_small:
		            sum_date[1] = missing_time.__str__()
		            sum_date[0] = prev_activity_table[most_detected_activity]
		            time_summ=time_summation(sum_date)
		            if time_summ == '00:00:00':
		                time_summ = '01:00:00'
		                time_diff_update = True
		            prev_activity_table[most_detected_activity] = time_summ
		            prev_date_arr = prev_date.__str__().split(' ')
		            prev_date_rev_arr = prev_date_arr[0].split('-')
		            prev_date_revert = prev_date_rev_arr[2] + '-' + prev_date_rev_arr[1] + '-' + prev_date_rev_arr[0]
		            writer.write(prev_date_revert +";" + prev_date_arr[1] + ";" + prev_activity_table.__str__() + "\n")
		            all_hours_activity[prev_date_revert + ";" + prev_date_arr[1]] = prev_activity_table
		            prev_activity_small = False
		            prev_missing_time = missing_time
		            activity_table = {}
		            if time_diff_update :
		                time_diff = '00:00:00'
		                time_diff_update =False
		                prev_activity_table = {}
		            time_diff = time_difference(str(time_diff) ,str(missing_time)).__str__()
		            activity_table[most_detected_activity] = '00:00:00'


		        sum_date[1] = time_diff.__str__()
		        sum_date[0] = activity_table[most_detected_activity]
		        activity_table[most_detected_activity] = time_summation(sum_date)

		        if smaller_than == False and exceed_time == True:
		            #  writer.write(line_arr[0] + ";" + line_arr[1] + activity_table.__str__() + "\n")
		            activity_table = {}


	    with open(self.file_name, 'a') as writer:
		prev_date_arr = prev_date.__str__().split(' ')
		prev_date_rev_arr = prev_date_arr[0].split('-')
		prev_date_revert = prev_date_rev_arr[2] + '-' + prev_date_rev_arr[1] + '-' + prev_date_rev_arr[0]
		all_hours_activity[prev_date_revert + ";" + prev_date_arr[1]] = activity_table
		writer.write(prev_date_revert + ";24:00:00;" + activity_table.__str__() + "\n")


	    

dataProcessing = DataProcessing('hourly_activity_minutes_se.txt')
day = '10-03-2021'
dataProcessing.activity_tables_for_24hours(file_name, day)
dataProcessing.days_of_logger()	    
