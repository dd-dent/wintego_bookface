import click
from scraper_config import BASE_URL
import trio
import asks
from pprint import pprint
asks.init('trio')


@click.command()
@click.argument('user-name', required=True)
@click.argument('password', required=True)
def main(user_name, password):
    trio.run(start_scraping, {'username': user_name, 'password': password})


async def start_scraping(credentials: dict):
    token = await login(credentials)
    if not token:
        exit(1)


async def login(credentials: dict) -> str:
    click.secho(f'attempting login to {BASE_URL}/api/login', fg='yellow')
    click.secho(f'credentials - {credentials}', fg='yellow')
    response = await asks.post(f'{BASE_URL}/api/login', json=credentials)
    status = response.status_code
    if status != 200:
        click.secho(
            f'login failed with status code: {status_code}', fg='red')
        return

    res_json = response.json()
    if res_json['status'] == 'failure':
        click.secho(f'login failed - reason: {res_json["reason"]}', fg='red')
        return
    token = response.cookies[0].value
    click.secho(f'login successful. token: {token}', fg='green')
    return token

if __name__ == "__main__":
    main()
