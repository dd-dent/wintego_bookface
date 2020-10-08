# bookface-scraper

Async BookFace API scraper

## Requirements

### Python

Tested on versions 3.6 and 3.7.

### OS

Tested on mac OS X Mojave and Ubuntu 16.04.5

## Installing

```bash
pip install .
```

## Building

```bash
pip install wheel
python setup.py build
```

This will create a `dist/bookface_scraper-[version]-py3-none-any.whl` file
where the version is taken from setup.py.  
To install the package: `pip install dist/bookface_scraper-[version]-py3-none-any.whl`

## Usage

### Run installed package

```bash
bookface-scraper USERNAME PASSWORD [-l, --limit]
```

### Run without packaging

```bash
cd PROJECT_DIR
PYTHONPATH=. python3 bookface_scraper/cli.py USERNAME PASSWORD [-l, --limit]
```

## Technical Overview

API access is controlled via the **api_client.Client** class, using an **asks.Session** instance to throttle the amount of concurrent connections and abstracting common API operations.  
The **user.User** class is used to deserialize users, to wit using the protobuf, base64 and bitwise operations to parse user profile information.
The scraper module manages the entire scraping process, instantiating the API client and housing the Scraper class.  
The **scraper.Scraper** class uses a trio nursery to throttle, scope and wait for tasks to finish, tasks being scraping individual users.
