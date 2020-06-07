import os, sys
import subprocess as sbp
from pprint import pprint
import environs



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



def main():
    env = environs.Env()
    env.read_env(recurse = False, verbose = True)
    cfg = parse_env()
    for envvar in cfg.keys():
        validate_var(env, envvar)
    

    



    


if __name__ == '__main__':
    main()
