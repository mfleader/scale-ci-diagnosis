import os, sys, re
import subprocess as sbp
from datetime import datetime as dt
from typing import Optional
from pprint import pprint
from enum import Enum
from pathlib import Path

import environs
import typer


app = typer.Typer()


class PrometheusCaptureType(str, Enum):
    none = 'none'
    wal = capture_wal
    full = capture_full_db


class Storage(str, Enum):
    local =  'local'
    pbench = 'pbench'
    data_server = 'data_server'


def split(s):
    return s.replace('\n', '').split('=')


def parse_env():
    with open('.env', 'r', encoding='utf-8') as f:
        return {k:v for k,v in (split(s) for s in f.readlines())}


def lines(stdout_str):
    return re.sub('[\t ]+', ' ', stdout_str) \
        .replace('\'', '') \
        .split('\n')


# def parse_pods(stdout_str):
#     matrix = [
#         line.spilt(' ') for line in lines(stdout_str) if len(line) > 0
#     ]
#     return pd.DataFrame(matrix[1:], columns = matrix[0])


# def get_prometheus_pod(df, index = -1):
#     return df \
#         [df['NAME'].str.contains('prometheus-k8s')] \
#         .query("STATUS == 'Running'") \
#         .iloc[index] \
#         ['NAME']


# def validate_var(env, varname):
#     if not env(varname):
#         print(f'Looks like {varname} is not defined, please check')
#         help()
#         typer.Exit()


def ts():
    return dt.utcnow().strftime('%Y%m%d-%H%M%S')


def validate_kubecfg(kubeconfig):
    # sbp.check_output to validate output
    # sbp.check_call to validate exit code
    if kubeconfig.stat().st_size == 0:
        typer.echo('KUBECONFIG var is undefined and cannot find kube config in the home directory, please check')
        raise typer.Exit(1)


def validate_oc():
    try:
        sbp.check_call(['which', 'oc', '&>/dev/null'])
    except sbp.CalledProcessError as err:
        typer.echo(err)
        typer.echo('oc client is not installed, please install')
        raise typer.Exit(1)
    


def capture_wal(namespace, pod, output_dir):
    src = 'wal'
    dest = src
    try:
        sbp.check_call([
            'oc', 'cp',
            f'{namespace}/{pod}:/prometheus/{src}',
            '--container', 'prometheus',
            f'{output_dir}/{dest}/'
        ])
        sbp.check_call([
            'XZ_OPT=--threads=0',
            'tar', 'cJf',
            f'{output_dir}/prometheus-{ts()}.tar.xz',
            '--directory', f'{output_dir}/{dest}', '.'
        ])
        sbp.check_call([
            'rm', '-fr', f'{output_dir}/{dest}'
        ])
    except sbp.CalledProcessError as err:
        typer.echo(err)
        raise typer.Exit(1)



def capture_full_db(namespace, pod, output_dir):
    src = ''
    dest = 'data'
    try:
        sbp.check_call([
            'oc', 'cp',
            f'{namespace}/{pod}:/prometheus/{src}',
            '--container', 'prometheus',
            f'{output_dir}/{dest}'
        ])
        sbp.check_call([
            'XZ_OPT=--threads=0',
            'tar', 'cJf',
            f'{output_dir}/prometheus-{ts()}.tar.xz',
            '--directory', f'{output_dir}/{dest}', '.'
        ])
        sbp.check_call([
            'rm', '-fr', f'{output_dir}/{dest}'
        ])
    except sbp.CalledProcessError as err:
        typer.echo(err)
        raise typer.Exit(1)


def must_gather(output_dir):
    try:
        sbp.check_call([
            'oc', 'adm', 'must-gather', 
            f"--dest-dir={output_dir}/must-gather-{ts()}"
        ])
    except sbp.CalledProcessError as err:
        typer.echo(err)
        raise typer.Exit(1)


def post_to_server():
    pass


def validate_server_is_up():
    pass


def set_pbench():
    pass


@app.command()
def pbench():
    result_dir = sbp.check_output([
        """
        ls -t /var/lib/pbench-agent/ | grep "pbench-user" | head -1
        """
    ])


@app.command()
def data_server():
    pass


def main(
    output_dir: Path,
    prometheus_capture_type: PrometheusCaptureType,
    mustgather: bool = False,
    kubeconfig: Path = typer.Option(
        Path(Path.home(), '.kube/config'),
        envvar = 'KUBECONFIG',
        callback = validate_kubecfg,
        prompt = True)
):
    typer.echo(output_dir)
    typer.echo(prometheus_capture_type)
    prometheus_namespace = 'openshift-monitoring'
    print(prometheus_namespace)
    # validated kubeconfig in header
    #
    # validate_oc()
    # get prometheus pod name


    # 3.8
    # prom_running = sbp.run(['oc', 'get', 'pods', '-n', prometheus_namespace], 
    #     capture_output=True,
    #     encoding='utf-8').stdout
    # print(prom_running)

    # ctz.pipe(
    #     prom_running,
    #     parse_pods,
    #     get_prometheus_pod,
    #     print
    # )

    

    if openshift_mustgather:
        must_gather(output_dir)







    


if __name__ == '__main__':
    typer.run(main)
