from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/SelikoW1983/superlists.git'

def deploy():
    '''развернуть'''
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    '''создать струткуру каталога, если нужно'''
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    '''получить самый свежий исходный код'''
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
    '''обновить настройки'''
    setting_path = source_folder +'/superlists/settings.py'
    sed(setting_path, "DEBUG = TRUE", "DEBUG = FALSE")
    sed(setting_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars)for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(setting_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    '''обновить виртуальную среду'''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.8 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    '''обновить статические файлы'''
    run(
       f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(sourse_folder):
    '''обновить базу данных'''
    run(
        f'cd {sourse_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

#import random
#from fabric.contrib.files import append, exists
#from fabric.api import cd, env, local, run

#REPO_URL = 'https://github.com/SelikoW1983/superlists.git'


#def deploy():
#    '''развернуть'''
#    site_folder = f'/home/{env.user}/sites/{env.host}'
#    run(f'mkdir -p {site_folder}')
#    with cd(site_folder):
#        _get_latest_source()
#        _update_virtualenv()
#        _create_or_update_dotenv()
#        _update_static_files()
#        _update_database()


#def _get_latest_source():
#    '''получить самый свежий исходный код'''
#    if exists('.git'):
#        run('git fetch')
#    else:
#        run(f'git clone {REPO_URL}')
#    current_commit = local("git log -n 1 --format=%H", capture=True)
#    run(f'git reset --hard {current_commit}')


#def _update_virtualenv():
#    '''обновить виртуальную среду'''
#    if not exists('virtualenv/bin/pip'):
#        run(f'python3.6 -m venv virtualenv')
#    run('./virtualenv/bin/pip install -r requirements.txt')


#def _create_or_update_dotenv():
#    '''обновить настройки'''
#    append('.env', 'DJANGO_DEBUG_FALSE=y')
#    append('.env', f'SITENAME={env.host}')
#    current_contents = run('cat .env')
#    if 'DJANGO_SECRET_KEY' not in current_contents:
#        new_secret = ''.join(random.SystemRandom().choices(
#            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
#        ))
#        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


#def _update_static_files():
#    '''обновить статисеские файлы'''
#    run('./virtualenv/bin/python manage.py collectstatic --noinput')


#def _update_database():
#    '''обновить базу данных'''
#    run('./virtualenv/bin/python manage.py migrate --noinput')
