import os, sys
import subprocess as sbp
from pprint import pprint
import environs
from openshift.dynamic import DynamicClient



def help():
    print('')
    print(f'Usage: python {sys.argv[0]}')


def split(s):
    return s.replace('\n', '').split('=')


def parse_env():
    with open('.env', 'r', encoding='utf-8') as f:
        return {k:v for k,v in (split(s) for s in f.readlines())}
        

def validate_var(env, varname):
    if not env(varname):
        print(f'Looks like {varname} is not defined, please check')
        help()
        os._exit(1)


def validate_kubecfg(env):
    if not env('KUBECONFIG') \
        and pathlib.Path(pathlib.Path.home(), '.kube/config') \ 
            .stat().st_size == 0:
        print('KUBECONFIG var is not defined and cannot find kube config in the home directory, please check')
        os._exit(1)


def validate_oc():
    if sbp.run(['which', 'oc', '&>/dev/null']).returncode != 0:
        print('oc client is not installed, please install')
        os._exit(1)
    else:
        print('oc client is present')


def capture_wal():
    pass


def capture_full_db():
    pass


def must_gather(env):
    sbp.run(['oc', 'adm', 'must-gather', '/'.join((env('OUTPUT_DIR')))])


def main():
    env = environs.Env()
    env.read_env(recurse = False, verbose = True)
    cfg = parse_env()
    for envvar in cfg.keys():
        validate_var(env, envvar)

    
    prometheus_pod = sbp.run([''])
    

    



    


if __name__ == '__main__':
    main()
