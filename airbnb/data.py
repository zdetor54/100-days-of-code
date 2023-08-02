
import pandas as pd
from datetime import datetime, timedelta

TOTAL_ALLOWANCE = 7500.00

class Reservations():
    def __init__(self, files_list: list):
        self.files = files_list
        self.directory = self.files[0]
        self.reservation_list = []
        self.reservation_data = {}
        self.reservation_df = pd.DataFrame()
        self.get_reservation_data()
        self.deduplicate_reservations()
        self.remaining_allowance = TOTAL_ALLOWANCE - self.reservation_df['Amount'].sum(axis='index')

    def get_reservation_data(self):
        for file in self.files:
            df = pd.read_csv(file)
            df = df[df.Type == 'Reservation'][['Confirmation Code', 'Guest', 'Listing', 'Start Date', 'Nights', 'Amount']]
            df['Nights'] = df['Nights'].apply(lambda row: int(row))
            df['Start Date'] = pd.to_datetime(df['Start Date'])
            df['End Date'] = df.apply(lambda x: x['Start Date'] + timedelta(days=x['Nights']), axis=1)
            df['Listing'] = df['Listing'].apply(lambda row: f"{row.split(' ')[0]} {row.split(' ')[1]}")
            self.reservation_df = pd.concat([self.reservation_df, df])


            df['Start Date'] = df['Start Date'].apply(lambda row: datetime.strftime(row, '%Y-%m-%d'))
            df['End Date'] = df['End Date'].apply(lambda row: datetime.strftime(row, '%Y-%m-%d'))
            # self.reservation_df = pd.concat([self.reservation_df, df])
            self.reservation_list += df[['Confirmation Code', 'Guest', 'Listing', 'Start Date', 'End Date', 'Nights', 'Amount']].to_dict(
                orient='records')
        self.reservation_list.sort(key=lambda x: x['Start Date'])


    def deduplicate_reservations(self):
        self.reservation_df = self.reservation_df.drop_duplicates(subset='Confirmation Code')
        self.reservation_df.set_index(keys= 'Confirmation Code', inplace=True)
        self.reservation_df = self.reservation_df.sort_values(by=['Start Date'])
        self.reservation_df = self.reservation_df.drop_duplicates()

        for element in self.reservation_list:
            temp_dict = {}
            temp_dict[element['Confirmation Code']] = element
            temp_dict[element['Confirmation Code']].pop('Confirmation Code')
            self.reservation_data.update(temp_dict)

    def get_reservations(self,period: str) -> pd.DataFrame:
        if period == 'Month':
            return self.reservation_df[self.reservation_df['Start Date'].map(lambda x: x.month) == datetime.now().month]
        elif period == 'MTD':
            return self.reservation_df[(self.reservation_df['Start Date'].map(lambda x: x.month) == datetime.now().month)
                                       & (self.reservation_df['Start Date'].map(lambda x: x.day) <= datetime.now().day)]
        elif period == 'Year':
            return self.reservation_df[self.reservation_df['Start Date'].map(lambda x: x.year) == datetime.now().year]
        elif period == 'YTD':
            return self.reservation_df[self.reservation_df['Start Date'] <= datetime.now()]
        elif 'Month+' in period:
            temp = int(period.split('+')[1])
            return self.reservation_df[self.reservation_df['Start Date'].map(lambda x: x.month) == datetime.now().month+temp]

