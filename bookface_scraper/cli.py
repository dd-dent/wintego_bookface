import click
import trio
import bookface_scraper.scraper as scraper
import json
import oyaml as yaml
import csv

@click.command()
@click.argument('user-name', required=True)
@click.argument('password', required=True)
@click.option('--limit', '-l', required=False, help='stop after X users', default=0)
def cli(user_name, password, limit):
    trio.run(start_scraping, {'username': user_name, 'password': password}, limit)


async def start_scraping(credentials: dict, limit):
    user_data = await scraper.get_users_data(credentials, limit)
    click.secho(f'finished scraping successfully', fg='green')
    # convert scraped data dictionary to a list, along with converting
    # all embedded sets to lists for easier serializing:
    results = []
    for key in user_data.keys():
        results.append(user_data[key].to_dict())
    
    # and dump results as JSON, YAML and CSV:
    with open('output.json', 'wt') as fd:
        json.dump(results, fd)
    with open('output.yml', 'wt') as fd:
        yaml.dump(results, fd)
    with open('output.csv', 'wt') as fd:
        writer = csv.DictWriter(fd, fieldnames=results[0].keys(), dialect=csv.unix_dialect)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    cli()
