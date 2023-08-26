import csv 

def write_csv(user_data, csv_filename):
  with open("user_data.csv", mode='w', newline='') as csv_file:
            fieldnames = ["name", "phone", "legal_age", "approved", "paid"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            csv_writer.writeheader()
            for user_info in user_data:
                csv_writer.writerow(user_info)