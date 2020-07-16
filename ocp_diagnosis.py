import os, sys, pathlib, re
import subprocess as sbp
from pprint import pprint
import environs
import typer

from enum import Enum


class PrometheusCaptureType(str, Enum):
    wal = 'wal'
    full = 'full'


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


def validate_var(env, varname):
    if not env(varname):
        print(f'Looks like {varname} is not defined, please check')
        help()
        os._exit(1)


def validate_kubecfg(env):
    if not env('KUBECONFIG') \
        and pathlib.Path(pathlib.Path.home(), '.kube/config').stat().st_size == 0:
        print('KUBECONFIG var is not defined and cannot find kube config in the home directory, please check')
        os._exit(1)


def validate_oc():
    if sbp.run(['which', 'oc', '&>/dev/null']).returncode != 0:
        print('oc client is not installed, please install')
        os._exit(1)
    else:
        print('oc client is present')


def copy_prom(type: str):
    pass


def capture_wal():
    pass


def capture_full_db():
    pass


def must_gather(output_dir):
    sbp.run(['oc', 'adm', 'must-gather', output_dir])


def main(
    output_dir: pathlib.Path,
    prometheus_capture_type: PrometheusCaptureType,
    prometheus_capture: bool = False,
    openshift_mustgather: bool = False,
    storage: Storage = typer.Option(Storage.local)
):
    typer.echo(output_dir)
    typer.echo(prometheus_capture_type)
    typer.echo(storage)


    prometheus_namespace = 'openshift-monitoring'


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







    


if __name__ == '__main__':
    typer.run(main)
