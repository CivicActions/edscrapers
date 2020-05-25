import os
import sys
import click
import importlib

from scrapy.crawler import CrawlerProcess
from loguru import logger
from pathlib import Path

from edscrapers.scrapers.base import config as scrape_config
from edscrapers.scrapers.base import helpers as scrape_base
from edscrapers.scrapers.base import helpers as scrape_helpers

from edscrapers.tools.dashboard import app as dash_app
from edscrapers.tools.stats.stats import Statistics

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

global_options=[
    click.option('-v', '--verbose', 'verbosity', count=True, help='Show INFO and DEBUG messages.'),
    click.option('-q', '--quiet', is_flag=True, default=False, help='Do not show anything.'),
    # click.option('-o', '--output', 'out_file_path', type=click.Path(), default=None,
    #              help='If specified, pipe the output to both STDOUT and the file specified.')
]

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

def _check_environment():
    errors = ['ED_OUTPUT_PATH']
    warnings = ['S3_ACCESS_KEY', 'S3_SECRET_KEY']

    for e in errors:
        if not os.getenv(e):
            logger.error(f'Environment variable {e} not set! Aborting.')
            sys.exit(1)

    for w in warnings:
        if not os.getenv(w):
            logger.warning(f'{w} not set.')


def setup_logger(quiet, verbosity, namespace, name=''):
    if not os.getenv('ED_OUTPUT_PATH'):
        logger.error('Environment variable ED_OUTPUT_PATH not set! Aborting.')

    log_levels = {'0': 'WARNING', '1': 'INFO', '2': 'DEBUG'}
    logger.remove()

    log_dir = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'logs')

    try:

        if not quiet:
            # Not quiet, so we can log to STDOUT
            logger.add(sys.stdout,
                    colorize=True,
                    level=log_levels[str(verbosity)],
                    # filter="edscrapers",
                    format="<level>{message}</level>",
                    backtrace=True,
                    diagnose=True)


        logger.add(os.path.join(log_dir, f'{namespace}_{name}'+'_{time}.log'),
                format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                filter="edscrapers",
                level=log_levels[str(verbosity)],
                # filter="edscrapers",
                enqueue=True,
                rotation="1 GB",
                backtrace=True,
                diagnose=True)
    except KeyError:
        setup_logger(quiet, 2, namespace, name)

    return True


@click.group()
def cli():
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('--cache/--no-cache', default=True, help='Do not use Scrapy cache (i.e. "live" scrape)')
@click.option('--resume/--no-resume', default=False, help='Resume a previously interrupted scrape')
@add_options(global_options)
@click.argument('name')
def scrape(cache, resume, name, **kwargs):
    '''Run a Scrapy pipeline for crawling / parsing / dumping output'''

    setup_logger(kwargs['quiet'], kwargs['verbosity'], 'scrapers', name)
    _check_environment()

    # Prepare conf dict
    conf = scrape_helpers.get_variables(scrape_config, str.isupper)

    # Get the crawler & start the scrape
    crawler = importlib.import_module(f'edscrapers.scrapers.{name}').Crawler

    if not cache:
        conf['SCRAPY_SETTINGS']['HTTPCACHE_ENABLED'] = False
    else:
        conf['SCRAPY_SETTINGS']['HTTPCACHE_ENABLED'] = True

    if kwargs['verbosity']:
        conf['SCRAPY_SETTINGS']['LOG_ENABLED'] = True
    else:
        conf['SCRAPY_SETTINGS']['LOG_ENABLED'] = False

    if resume:
        job_dir = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'scrapy', 'jobs')
        cache_dir = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'scrapy', 'httpcache')

        Path(job_dir).mkdir(parents=True, exist_ok=True)
        Path(cache_dir).mkdir(parents=True, exist_ok=True)

        conf['SCRAPY_SETTINGS']['JOBDIR'] = job_dir
        conf['SCRAPY_SETTINGS']['HTTPCACHE_DIR'] = cache_dir


    process = CrawlerProcess(conf['SCRAPY_SETTINGS'])
    process.crawl(crawler)
    process.start()


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', 'in_file_path', type=click.Path(exists=True), default=None,
              help=''' Input file, if used by requested transformer (e.g. datajson transformer
              can use a dedup output) If a directory will be provided instead, it will be
              traversed recursivelly to obtain the list of files.''')
@click.option('-n', '--name', default=None,
              help='''If specified, the transformer will only act on the mentioned output (i.e. a scraper's name)''')
@click.argument('transformer')
@add_options(global_options)
def transform(in_file_path, name, transformer, **kwargs):
    '''Run a transformer on a scraper output to generate data in a format useful for other applications'''
    setup_logger(kwargs['quiet'], kwargs['verbosity'], 'transformers', transformer)
    _check_environment()
    transformer = importlib.import_module(f"edscrapers.transformers.{transformer}.transform")
    transformer.transform(name, in_file_path)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-n', '--name', default=None,
              help='Optionally, run the stats just for a specific output pipeline, identified by name (e.g. nces)')
@click.option('-f', '--format', default=None, type=click.Choice(['ascii', 'json'], case_sensitive=False),
              help='Format of the output.')
@add_options(global_options)
def stats(name, **kwargs):
    ''' Run a statistics algorhitm on the data extracted to provide more insights about the output.'''
    click.echo('Making stats')

    #data_dir = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'data')
    #Path(data_dir).mkdir(parents=True, exist_ok=True)

    stats = Statistics(delete_all_stats=True)
    stats.generate_statistics()
    logger.success('Stats complete!')


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-d', 'detached', is_flag=True, default=False, help='Run the server in a detached process')
@click.option('--debug', 'debug', is_flag=True, default=False, help='Flag for turning debug mode on')
@click.option('-p', '--port', 'port', type=click.INT, default=8050, help='Change the server port (default is 8050)')
@click.option('-h', '--host', 'host', default='0.0.0.0', help='Change the server host (default is 0.0.0.0)')
@add_options(global_options)
def dash(detached, port, host, debug, **kwargs):
    ''' Run the dash server for displaying HTML statistics. '''
    setup_logger(kwargs['quiet'], kwargs['verbosity'], 'dash')
    if detached:
        logger.warning('Dash app detached mode not yet implemented!')
        logger.info('Falling back to non-detached mode.')
    dash_app.app.run_server(debug=debug, dev_tools_hot_reload=debug, host=host)



if __name__ == '__main__':
    cli()
