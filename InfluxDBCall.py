from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
import pytz
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


class InfluxCall:
    # Define InfluxDB connection parameters
    url = "http://192.168.0.5:8086"  # Replace with your InfluxDB URL
    token = "gNqBY_gn_fN4MBbgaLtcvHE7eMT-J2gKyQuMXn9J6Qr3tFjbKyPBbKaznCGQnPJsnZdvLKEbRkVCAf-ZsPq7Rg=="  # Replace with your InfluxDB token
    org = "org_rech"  # Replace with your InfluxDB organization
    bucket = "bucket_rech"  # Replace with your InfluxDB bucket

    def __init__(self):
        self.client = InfluxDBClient(url=InfluxCall.url, token=InfluxCall.token, org=InfluxCall.org)
        self.query_api = self.client.query_api()

        try:
            self.client.ping()
            logging.info("Connected to InfluxDB!")
        except Exception as e:
            logging.warning("Unable to connect to InfluxDB:", str(e))

    @staticmethod
    def _is_within_margin(datetime_to_check, margin_minutes=5):
        # Get current date and time in UTC timezone
        current_datetime = datetime.now(pytz.utc)

        # Convert the given datetime to UTC timezone if it's not already timezone-aware
        if datetime_to_check.tzinfo is None or datetime_to_check.tzinfo.utcoffset(datetime_to_check) is None:
            datetime_to_check = datetime_to_check.replace(tzinfo=pytz.utc)

        # Calculate the margin of error
        margin_error = timedelta(minutes=margin_minutes)

        # Calculate the lower and upper bounds for comparison
        lower_bound = current_datetime - margin_error
        upper_bound = current_datetime + margin_error

        # Check if the given datetime is within the margin of error
        return lower_bound <= datetime_to_check <= upper_bound


    def get_active_power(self):

        query = f'''
        from(bucket: "{InfluxCall.bucket}")
          |> range(start: -1d)  // Adjust the time range as needed
          |> filter(fn: (r) => r["_measurement"] == "power")
          |> filter(fn: (r) => r["_field"] == "total_active_power")
          |> filter(fn: (r) => r["inverter"] == "SG12RT" or r["inverter"] == "SG40RS")
          |> last()
        '''

        # Run the Flux query
        result = self.query_api.query(org=InfluxCall.org, query=query)

        # Process and print the results
        total_power = 0
        for table in result:
            for row in table.records:
                if InfluxCall._is_within_margin(row.get_time()): #Check if entries are from within the last 5 minutes
                    total_power += row.get_value()
                else:
                    logging.warning(f'Last entry timestamp: {row.get_time()}, does not match current time {datetime.now(pytz.utc)}, for Inverter: {row["inverter"]}. Returning 0 Power')
        return total_power

if __name__ == "__main__":

    influxi = InfluxCall()
    print(influxi.get_active_power())
#
# leistung, parsed_time = get_Leistung_from_influx(client)
#
# while leistung == 0 and check_day(parsed_time, ) and temp < 60:
#     leistung, parsed_time = get_Leistung_from_influx(client)
#     print("dates are the same")
#     print(check_day(parsed_time, datetime.today()))


