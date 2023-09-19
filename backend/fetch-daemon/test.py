# Import libraries
import betfairlightweight
from betfairlightweight import filters
import pandas as pd
import numpy as np
import os
import datetime
import json

with open('credentials.json') as f:
    cred = json.load(f)
    my_username = cred['username']
    my_password = cred['password']
    my_app_key = cred['app_key']
    certs_path = cred['certs_path']

trading = betfairlightweight.APIClient(username=my_username,
                                       password=my_password,
                                       app_key=my_app_key,
                                       certs=certs_path)

trading.login()

event_types = trading.betting.list_event_types()
sport_ids = pd.DataFrame({
    'Sport': [event_type_object.event_type.name for event_type_object in event_types],
    'ID': [event_type_object.event_type.id for event_type_object in event_types]
}).set_index('Sport').sort_index()

print ("sports ids ==> \n", sport_ids)

# Filter for just horse racing
horse_racing_filter = betfairlightweight.filters.market_filter(text_query='Horse Racing')

# This returns a list
horse_racing_event_type = trading.betting.list_event_types(filter=horse_racing_filter)

# Get the first element of the list
horse_racing_event_type = horse_racing_event_type[0]

horse_racing_event_type_id = horse_racing_event_type.event_type.id
print(f"The event type id for horse racing is {horse_racing_event_type_id}")

# Get a datetime object in a week and convert to string
datetime_in_a_week = (datetime.datetime.utcnow() + datetime.timedelta(weeks=1)).strftime("%Y-%m-%dT%TZ")

# Create a competition filter
competition_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[horse_racing_event_type_id], # Horse Racing's event type id is 7
    market_start_time={
        'to': datetime_in_a_week
    })

# Get a list of competitions for Horse Racing
competitions = trading.betting.list_competitions(
    filter=competition_filter
)

# Iterate over the competitions and create a dataframe of competitions and competition ids
horse_racing_competitions = pd.DataFrame({
    'Competition': [competition_object.competition.name for competition_object in competitions],
    'ID': [competition_object.competition.id for competition_object in competitions]
})
print (horse_racing_competitions)

thoroughbreds_event_filter = betfairlightweight.filters.market_filter(
    event_type_ids=[horse_racing_event_type_id],
    market_countries=['AU'],
    market_start_time={
        'to': (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%TZ")
    }
)
print ("thoroughbreds_event_filter ===> ", thoroughbreds_event_filter)

# Get a list of all thoroughbred events as objects
aus_thoroughbred_events = trading.betting.list_events(
    filter=thoroughbreds_event_filter
)

# Create a DataFrame with all the events by iterating over each event object
aus_thoroughbred_events_today = pd.DataFrame({
    'Event Name': [event_object.event.name for event_object in aus_thoroughbred_events],
    'Event ID': [event_object.event.id for event_object in aus_thoroughbred_events],
    'Event Venue': [event_object.event.venue for event_object in aus_thoroughbred_events],
    'Country Code': [event_object.event.country_code for event_object in aus_thoroughbred_events],
    'Time Zone': [event_object.event.time_zone for event_object in aus_thoroughbred_events],
    'Open Date': [event_object.event.open_date for event_object in aus_thoroughbred_events],
    'Market Count': [event_object.market_count for event_object in aus_thoroughbred_events]
})

print ("aus_thoroughbred_events_today ===> ", aus_thoroughbred_events_today)

# Define a market filter
market_types_filter = betfairlightweight.filters.market_filter(event_type_ids=[horse_racing_event_type_id])

# Request market types
market_types = trading.betting.list_market_types(
        filter=market_types_filter
)

# Create a DataFrame of market types
market_types_mooney_valley = pd.DataFrame({
    'Market Type': [market_type_object.market_type for market_type_object in market_types],
})

print ("market_types_mooney_valley ===> ", market_types_mooney_valley)

market_catalogue_filter = betfairlightweight.filters.market_filter(event_type_ids=[horse_racing_event_type_id])

market_catalogues = trading.betting.list_market_catalogue(
    filter=market_catalogue_filter,
    max_results='100',
    sort='FIRST_TO_START'
)

# Create a DataFrame for each market catalogue
market_types_mooney_valley = pd.DataFrame({
    'Market Name': [market_cat_object.market_name for market_cat_object in market_catalogues],
    'Market ID': [market_cat_object.market_id for market_cat_object in market_catalogues],
    'Total Matched': [market_cat_object.total_matched for market_cat_object in market_catalogues],
})

print ("market_types_mooney_valley ===> ", market_types_mooney_valley)

def process_runner_books(runner_books):
    '''
    This function processes the runner books and returns a DataFrame with the best back/lay prices + vol for each runner
    :param runner_books:
    :return:
    '''
    best_back_prices = [runner_book.ex.available_to_back[0]['price']
        if runner_book.ex.available_to_back
        else 1.01
        for runner_book
        in runner_books]
    best_back_sizes = [runner_book.ex.available_to_back[0]['size']
        if runner_book.ex.available_to_back
        else 1.01
        for runner_book
        in runner_books]

    best_lay_prices = [runner_book.ex.available_to_lay[0]['price']
        if runner_book.ex.available_to_lay
        else 1000.0
        for runner_book
        in runner_books]
    best_lay_sizes = [runner_book.ex.available_to_lay[0]['size']
        if runner_book.ex.available_to_lay
        else 1.01
        for runner_book
        in runner_books]

    selection_ids = [runner_book.selection_id for runner_book in runner_books]
    last_prices_traded = [runner_book.last_price_traded for runner_book in runner_books]
    total_matched = [runner_book.total_matched for runner_book in runner_books]
    statuses = [runner_book.status for runner_book in runner_books]
    scratching_datetimes = [runner_book.removal_date for runner_book in runner_books]
    adjustment_factors = [runner_book.adjustment_factor for runner_book in runner_books]

    df = pd.DataFrame({
        'Selection ID': selection_ids,
        'Best Back Price': best_back_prices,
        'Best Back Size': best_back_sizes,
        'Best Lay Price': best_lay_prices,
        'Best Lay Size': best_lay_sizes,
        'Last Price Traded': last_prices_traded,
        'Total Matched': total_matched,
        'Status': statuses,
        'Removal Date': scratching_datetimes,
        'Adjustment Factor': adjustment_factors
    })
    return df

# Create a price filter. Get all traded and offer data
price_filter = betfairlightweight.filters.price_projection(
    price_data=['EX_BEST_OFFERS']
)

# Request market books
market_books = trading.betting.list_market_book(
    market_ids=['1.150038686'],
    price_projection=price_filter
)

# Grab the first market book from the returned list as we only requested one market 
market_book = market_books[0]

runners_df = process_runner_books(market_book.runners)

print ("runners_df === > ", runners_df)
