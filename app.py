import streamlit as st
import pickle
import pandas as pd
import sys
from titlecase import titlecase


def preprocess_high_null_values(df):
    df['maneuver_missing_info?'] = df['MANOEUVER'].isnull().replace({True: 'Yes', False: 'No'})
    df['pedtype_missing_info?'] = df['PEDTYPE'].isnull().replace({True: 'Yes', False: 'No'})
    df['cycact_missing_info?'] = df['CYCACT'].isnull().replace({True: 'Yes', False: 'No'})
    df['drivact_missing_info?'] = df['DRIVACT'].isnull().replace({True: 'Yes', False: 'No'})
    df.drop(['MANOEUVER', 'PEDTYPE', 'CYCACT', 'DRIVACT'], axis=1, inplace=True)
    return df
def categorize_age(X):
    def age_category(age_range):
        if age_range in ['0 to 4', '5 to 9', '10 to 14']:
            return 'kid'
        elif age_range == '15 to 19':
            return 'teenager'
        elif age_range in ['20 to 24', '25 to 29']:
            return 'youth'
        elif age_range in ['30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64']:
            return 'adult'
        elif age_range in ['65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90 to 94', 'Over 95']:
            return 'old'
        else:
            return 'unknown'
    transformed_column = X.iloc[:, 0].apply(age_category)
    return pd.DataFrame(transformed_column, columns=[X.columns[0]])

def frequency_encode(X):
    freq = X.iloc[:, 0].value_counts(normalize=True)
    transformed_column = X.iloc[:, 0].map(freq)
    return pd.DataFrame(transformed_column, columns=[X.columns[0]])

sys.modules['__main__'].preprocess_high_null_values = preprocess_high_null_values
sys.modules['__main__'].categorize_age = categorize_age
sys.modules['__main__'].frequency_encode = frequency_encode

# @st.cache(suppress_st_warning=True)
# @st.cache(allow_output_mutation=True)
def load_model():
    with open('final_model_pipeline.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

def create_selectbox(key, options):
    """Helper function to create a select box with titlecase label."""
    return st.selectbox(titlecase(key.replace('_', ' ')), ["Select"] + options)

def main():
    st.title('Accident Severity Prediction')

    # Define your form in the sidebar or main page area
    with st.form("prediction_form"):
        # Dictionary comprehension to create form fields dynamically
        inputs = {key: create_selectbox(key, values) for key, values in unique_values.items()}

        # Submit button for the form
        submitted = st.form_submit_button("Submit Prediction")
        if submitted:
            # Check if all fields have a selection other than "Select"
            # if all(value != "Select" for value in inputs.values()):
            # Prepare data for prediction
            data = pd.DataFrame([inputs])
            prediction = model.predict(data)
            result = 'Fatal' if prediction[0] == 1 else 'Non-fatal'
            st.success(f"The predicted accident severity is: {result}.")
            # else:
            #     st.error("Please fill in all fields to predict the accident severity.")

if __name__ == "__main__":
    unique_values = {
        "ROAD_CLASS": ['Major Arterial', 'Minor Arterial', 'Collector', 'Local', 'Expressway', 'Laneway', 'Other', 'Expressway Ramp', 'Pending'],
        "DISTRICT": ['Scarborough', 'North York', 'Toronto and East York', 'Etobicoke York'],
        "LOCCOORD": ['Intersection', 'Mid-Block', 'Mid-Block (Abnormal)', 'Exit Ramp Southbound', 'Entrance Ramp Westbound', 'Park, Private Property, Public Lane', 'Exit Ramp Westbound'],
        "TRAFFCTL": ['Traffic Signal', 'No Control', 'Stop Sign', 'Traffic Controller', 'Pedestrian Crossover', 'Yield Sign', 'Streetcar (Stop for)', 'Traffic Gate', 'Police Control'],
        "VISIBILITY": ['Clear', 'Rain', 'Other', 'Fog, Mist, Smoke, Dust', 'Snow', 'Freezing Rain', 'Strong wind', 'Drifting Snow'],
        "LIGHT": ['Daylight', 'Dark, artificial', 'Dark', 'Dusk, artificial', 'Daylight, artificial', 'Dawn, artificial', 'Dawn', 'Dusk', 'Other'],
        "RDSFCOND": ['Dry', 'Wet', 'Other', 'Loose Snow', 'Packed Snow', 'Loose Sand or Gravel', 'Ice', 'Slush', 'Spilled liquid'],
        "IMPACTYPE": ['Turning Movement', 'SMV Other', 'Sideswipe', 'Pedestrian Collisions', 'Cyclist Collisions', 'Approaching', 'Angle', 'SMV Unattended Vehicle', 'Rear End', 'Other'],
        "INVTYPE": ['Passenger', 'Driver - Not Hit', 'Driver', 'Pedestrian', 'Motorcycle Driver', 'Cyclist', 'Other Property Owner', 'Vehicle Owner', 'Truck Driver', 'Wheelchair', 'Motorcycle Passenger', 'Moped Driver'],
        "INVAGE": ['85 to 89', 'unknown', '55 to 59', '35 to 39', '40 to 44', '20 to 24', '60 to 64', '70 to 74', '45 to 49', '30 to 34', '10 to 14', '65 to 69', '50 to 54', '25 to 29', '15 to 19', '75 to 79', 'Over 95', '80 to 84', '0 to 4', '5 to 9', '90 to 94'],
        "INJURY": ['Fatal', 'Major', 'Minimal', 'Minor'],
        "INITDIR": ['Unknown', 'East', 'West', 'South', 'North'],
        "MANOEUVER": ['Stopped', 'Going Ahead', 'Turning Left', 'Slowing or Stopping', 'Reversing', 'Turning Right', 'Unknown', 'Other', 'Making U Turn', 'Changing Lanes', 'Parked', 'Overtaking', 'Pulling Away from Shoulder or Curb', 'Merging', 'Pulling Onto Shoulder or towardCurb'],
        "DRIVACT": ['Driving Properly', 'Lost control', 'Failed to Yield Right of Way', 'Improper Turn', 'Exceeding Speed Limit', 'Disobeyed Traffic Control', 'Other', 'Improper Lane Change', 'Following too Close', 'Speed too Fast For Condition', 'Improper Passing', 'Wrong Way on One Way Road', 'Speed too Slow'],
        "PEDTYPE": ['Vehicle is going straight thru inter.while ped cross without ROW', 'Pedestrian hit on sidewalk or shoulder', 'Vehicle turns left while ped crosses with ROW at inter.', 'Pedestrian involved in a collision with transit vehicle anywhere along roadway', 'Pedestrian hit at mid-block', 'Vehicle is reversing and hits pedestrian', 'Vehicle turns right while ped crosses with ROW at inter.', 'Other / Undefined', 'Pedestrian hit at private driveway', 'Vehicle turns left while ped crosses without ROW at inter.', 'Vehicle is going straight thru inter.while ped cross with ROW', 'Pedestrian hit a PXO/ped. Mid-block signal', 'Unknown', 'Vehicle hits the pedestrian walking or running out from between parked vehicles at mid-block', 'Vehicle turns right while ped crosses without ROW at inter.'],
        "CYCACT": ['Driving Properly', 'Disobeyed Traffic Control', 'Other', 'Improper Passing', 'Lost control', 'Improper Lane Change', 'Improper Turn', 'Failed to Yield Right of Way', 'Speed too Fast For Condition', 'Wrong Way on One Way Road'],
        "PEDESTRIAN": ['No', 'Yes'],
        "CYCLIST": ['No', 'Yes'],
        "AUTOMOBILE": ['No', 'Yes'],
        "MOTORCYCLE": ['No', 'Yes'],
        "TRUCK": ['No', 'Yes'],
        "TRSN_CITY_VEH": ['No', 'Yes'],
        "PASSENGER": ['No', 'Yes'],
        "SPEEDING": ['No', 'Yes'],
        "AG_DRIV": ['No', 'Yes'],
        "REDLIGHT": ['No', 'Yes'],
        "ALCOHOL": ['No', 'Yes'],
        "NEIGHBOURHOOD_158": ['Wexford/Maryvale', 'Flemingdon Park', 'Newtonbrook East', 'St Lawrence-East Bayfront-The Islands', 'Banbury-Don Mills',
        'Cabbagetown-South St.James Town', 'Kennedy Park', 'Yonge-Bay Corridor', 'Kingsview Village-The Westway', 'Rexdale-Kipling', 'Morningside',
        'Little Portugal', 'Weston', 'Moss Park', 'Humbermede', "Tam O'Shanter-Sullivan", 'West Rouge', 'Stonegate-Queensway', 'Clanton Park', "O'Connor-Parkview",
        'Morningside Heights', 'Oakdale-Beverley Heights', 'South Riverdale', 'West Humber-Clairville', 'Old East York', 'Don Valley Village', 'Woburn North', 'Lawrence Park South', 'Pleasant View', 'Newtonbrook West', 'Thistletown-Beaumond Heights', 'Forest Hill North', 'Casa Loma', 'Dovercourt Village', 'Clairlea-Birchmount',
            'Victoria Village', 'Islington', 'Rosedale-Moore Park', 'Bathurst Manor', 'Malvern West', 'North St.James Town', 'Caledonia-Fairbank', 'Willowridge-Martingrove-Richview',
            'NSA', 'South Parkdale', 'Weston-Pelham Park', 'Malvern East', 'Etobicoke City Centre', 'Harbourfront-CityPlace', 'Briar Hill-Belgravia', 'Henry Farm', 'Bedford Park-Nortown',
            'Centennial Scarborough', 'Mimico-Queensway', 'Fort York-Liberty Village', 'Runnymede-Bloor West Village', 'High Park North', 'Yonge-Eglinton', 'Oakridge', 'Westminster-Branson',
            'Eglinton East', 'Leaside-Bennington', 'Yorkdale-Glen Park', 'Humber Summit', 'Long Branch', 'Black Creek', 'East End-Danforth', 'Yonge-St.Clair', 'Lawrence Park North',
                'Edenbridge-Humber Valley', "East L'Amoreaux", 'High Park-Swansea', 'Lansing-Westgate', 'Dorset Park', 'Regent Park', 'Birchcliffe-Cliffside', 'Humber Bay Shores', 'Bendale South', 
                'Keelesdale-Eglinton West', 'Roncesvalles', 'Steeles', 'Golfdale-Cedarbrae-Woburn', 'Mount Pleasant East', 'Mount Olive-Silverstone-Jamestown', 'Princess-Rosethorn',
                'Playter Estates-Danforth', 'Downsview', 'Bendale-Glen Andrew', 'Humber Heights-Westmount', 'Taylor-Massey', 'Annex', 'Junction-Wallace Emerson', 'Ionview', 'Bayview Village', 
                'Bayview Woods-Steeles', 'Dufferin Grove', 'University', 'Oakwood Village', 'North Riverdale', 'Trinity-Bellwoods', 'East Willowdale', 'Cliffcrest', 'York University Heights', 
                'Wellington Place', 'Broadview North', 'Rockcliffe-Smythe', 'Woodbine Corridor', 'Kensington-Chinatown', 'Agincourt North', 'Bay-Cloverhill', 'Eringate-Centennial-West Deane', 
                'Willowdale West', 'Brookhaven-Amesbury', 'Danforth East York', 'Agincourt South-Malvern West', 'The Beaches', 'Glenfield-Jane Heights', 'Woodbine-Lumsden', 'Downtown Yonge East',
                'North Toronto', 'Bridle Path-Sunnybrook-York Mills', 'Greenwood-Coxwell', 'Yonge-Doris', 'St.Andrew-Windfields', 'Junction Area', "L'Amoreaux West", 'Milliken', 'Markland Wood', 
                'Blake-Jones', 'New Toronto', 'South Eglinton-Davisville', 'Alderwood', 'Wychwood', 'Hillcrest Village', 'West Hill', 'Corso Italia-Davenport', 'West Queen West', 'Mount Dennis', 
                'Palmerston-Little Italy', 'Rustic', 'Kingsway South', "Parkwoods-O'Connor Hills", 'Pelmo Park-Humberlea', 'Beechborough-Greenbrook', 'Elms-Old Rexdale', 'Maple Leaf', 'Highland Creek', 
                'Humewood-Cedarvale', 'Scarborough Village', 'Avondale', 'Fenside-Parkwoods', 'Englemount-Lawrence', 'Church-Wellesley', 'Thorncliffe Park', 'Etobicoke West Mall', 'Guildwood',
                'Forest Hill South', 'Danforth', 'Lambton Baby Point']
    }
    main()
