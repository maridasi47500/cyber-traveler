
mkdir templates 
python3 scaffold.py user username country_id:references email password phone
python3 scaffold.py country name
python3 scaffold.py data user_id:references name value
python3 scaffold.py device name
python3 scaffold.py userhasdevice device_id:references user_id:references
python3 scaffold.py airport short_name name city_id:references
python3 scaffold.py city name country_id:references
python3 scaffold.py userflights airport1_id airport2_id date heure number airline_company_id:references  user_id:references
python3 scaffold.py airline_company name
python3 scaffold.py conversations userhasdevice_id:references sender receiver description
