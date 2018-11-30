import click
import trio
import scraper


@click.command()
@click.argument('user-name', required=True)
@click.argument('password', required=True)
def cli(user_name, password):
    trio.run(start_scraping, {'username': user_name, 'password': password})


async def start_scraping(credentials: dict):
    user_data = await scraper.scrape(credentials)


if __name__ == "__main__":
    cli()
