# For those who don't want to keep refreshing Apple's Refurbished Product page

This script will keep checking Apple's API to check its product availability.
When it's available, it will send an email to yourself.
Now, you can buy those overpriced products at a _slightly_ better price. (Though still overpriced)

## Running instructions

- Set up dependencies
```
python3 -m virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

- Run `track.py`
```
python track.py
```

- Insert your email and password accordingly when prompted.

- To avoid typing your email and password everytime, store them in env var before running `track.py`
```
export EMAIL="something@gmail.com"
export EP={your_password}
```
