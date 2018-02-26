#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging
import os
import sys

from laika.reports import Config, Runner


ENV_LAIKA_CONFIG = 'LAIKA_CONFIG_FILE_PATH'
ENV_LAIKA_PWD = 'LAIKA_PWD'


@click.command('run', short_help='runs the report', context_settings=dict(
                    help_option_names=['-h', '--help'], allow_extra_args=True,
                    ignore_unknown_options=True))
@click.argument('report', default=None, required=False)
@click.option('-c', '--config', default=None, help='config file to use')
@click.option('-a', '--all', 'run_all', is_flag=True, help='run all reports')
@click.option('-l', '--list', 'show_list', is_flag=True, help='list available reports')
@click.option('--loglevel', default='INFO', help='level of log messages')
@click.option('--pwd', required=False)
@click.pass_context
def run(ctx, report, run_all, config, show_list, loglevel, pwd):
    """
    Runs report, specified in the config file.

    You can run all the listed reports, passing --all flag (don't pass report
    in this case). For the configuration, config.json is used by default, but
    you can specify another file with --config option.
    """

    current_path = os.path.dirname(os.path.realpath(__file__))
    config = config or os.environ.get(ENV_LAIKA_CONFIG) or current_path + '/config.json'
    logging.basicConfig(format='[%(asctime)s] %(name)s:%(levelname)s - %(message)s',
                        stream=sys.stdout, level=getattr(logging, loglevel), datefmt='%Y-%m-%d %H:%M:%S')

    pwd = pwd or os.environ.get(ENV_LAIKA_PWD) or current_path
    conf = Config(config, pwd)

    if show_list:
        click.echo(('Reports available: \n\n\t- ' +
                    '\n\t- '.join(sorted(conf.get_available_reports()))) + '\n')

    extra_args = dict(zip(*2 * [iter(a.replace('--', '') for a in ctx.args)]))
    runner = Runner(conf, **extra_args)
    if report:
        runner.run_report(report)
    elif run_all:
        runner.run()
    else:
        click.echo('Please, specify the report to run. Run with -h to see help message.')


if __name__ == '__main__':
    run()
