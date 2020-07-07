import os, sys, pathlib
import subprocess as sbp
from pprint import pprint
import environs
import cytoolz as ctz


def help():
    print('')
    print(f'Usage: python {sys.argv[0]}')


def split(s):
    return s.replace('\n', '').split('=')


def parse_env():
    with open('.env', 'r', encoding='utf-8') as f:
        return {k:v for k,v in (split(s) for s in f.readlines())}


def lines(stdout_str):
    return re.sub('[\t ]+', ' ', stdout_str) \
        .replace('\'', '') \
        .split('\n')


def parse_pods(stdout_str):
    matrix = [
        line.spilt(' ') for line in lines(stdout_str) if len(line) > 0
    ]
    return pd.DataFrame(matrix[1:], columns = matrix[0])


def get_prometheus_pod(df, index = -1):
    return df \
        [df['NAME'].str.contains('prometheus-k8s')] \
        .query("STATUS == 'Running'") \
        .iloc[index] \
        ['NAME']


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
    sbp.run([
        'oc', 'cp',
        f"{prometheus_namespace}/{prometheus_pod}:/prometheus/wal", 
        '-c', 'prometheus', f"{OUTPUT_DIR}/wal/"])
    
    # XZ_OPT=--threads=0 tar cJf $OUTPUT_DIR/prometheus-$ts.tar.xz $OUTPUT_DIR/wal
	# if [[ $? -eq 0 ]]; then
	# 	rm -rf $OUTPUT_DIR/wal
	# fi
    pass


def capture_full_db():
    pass


def must_gather(env):
    sbp.run(['oc', 'adm', 'must-gather', '/'.join((env('OUTPUT_DIR')))])


def main():
    # setup environment
    env = environs.Env()
    env.read_env(recurse = False, verbose = True)

    # parse provided environment variables
    cfg = parse_env()

    # validate environment variables
    for envvar in cfg.keys():
        validate_var(env, envvar)


    validate_kubecfg()
    validate_oc()

    prometheus_namespace = 'openshift-monitoring'

    # 3.6
    # sbp.run(['oc', 'get', 'pods', '-n', prometheus_namespace], stdout=sbp.PIPE).stdout

    # 3.8
    prom_running = sbp.run(['oc', 'get', 'pods', '-n', prometheus_namespace], 
        capture_output=True,
        encoding='utf-8').stdout
    print(prom_running)

    ctz.pipe(
        prom_running,
        parse_pods,
        get_prometheus_pod,
        print
    )







    


if __name__ == '__main__':
    main()
