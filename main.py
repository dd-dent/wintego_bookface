import click
import trio
import scraping_manager


@click.command()
@click.argument('user-name', required=True)
@click.argument('password', required=True)
def main(user_name, password):
    trio.run(start_scraping, {'username': user_name, 'password': password})


async def start_scraping(credentials: dict):
    manager = await scraping_manager.get_manager()


if __name__ == "__main__":
    main()
