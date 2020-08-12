#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging
import os
import sys
import json

# Temporary fix to use script having same name as the module
if os.path.dirname(os.path.realpath(__file__)) == sys.path[0]:
    sys.path.pop(0)

import laika


ENV_LAIKA_CONFIG = 'LAIKA_CONFIG_FILE_PATH'
ENV_LAIKA_PWD = 'LAIKA_PWD'


@click.command('run', short_help='runs the report', context_settings=dict(
                    help_option_names=['-h', '--help'], allow_extra_args=True,
                    ignore_unknown_options=True))
@click.version_option(version=laika.__version__)
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

    pwd = pwd or os.environ.get(ENV_LAIKA_PWD)
    config = config or os.environ.get(ENV_LAIKA_CONFIG)

    if not config and not pwd:
        import pkg_resources
        pwd = pkg_resources.resource_filename('laika', 'examples/')
        config = os.path.join(pwd, 'config.json')
        click.secho('Config file not specified, running with example configuration!', fg='yellow')

    logging.basicConfig(format='[%(asctime)s] %(name)s:%(levelname)s - %(message)s',
                        stream=sys.stdout, level=getattr(logging, loglevel), datefmt='%Y-%m-%d %H:%M:%S')

    conf = laika.Config(config, pwd)

    if show_list:
        click.echo(('Reports available: \n\n\t- ' +
                    '\n\t- '.join(sorted(conf.get_available_reports()))) + '\n')

    extra_args = dict(zip(*2 * [iter(a.replace('--', '') for a in ctx.args)]))

    if 'variables' in extra_args:
        extra_args['variables'] = json.loads(extra_args['variables'])

    conf.overwrite_attributes(extra_args)

    runner = laika.Runner(conf, **extra_args)
    if report:
        runner.run_report(report)
    elif run_all:
        runner.run()
    else:
        click.echo('Please, specify the report to run. Run with -h to see help message.')


if __name__ == '__main__':
    run()
