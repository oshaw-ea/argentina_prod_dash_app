import os
from invoke import task
#
# ARTIFACT_REGISTRY_LINKS = [
#     'https://europe-west2-python.pkg.dev/ea-us-production/ea-hf/simple',
#     'https://europe-west2-python.pkg.dev/ea-us-production/us-prod-model/simple'
# ]
#
#
# def _get_extra_indexes_string():
#     template = '--extra-index-url {link}'
#     links = []
#     for link in ARTIFACT_REGISTRY_LINKS:
#         links.append(template.format(link=link))
#     return ' '.join(links)

@task
def req_compile(ctx):
    '''
    Compile Python requirements without upgrading.
    '''
    ctx.run(f'pip-compile requirements/requirements.in')



# @task
# def req_compile(ctx):
#     '''
#     Compile Python requirements without upgrading.
#     '''
#     extra_index_string = _get_extra_indexes_string()
#     ctx.run(f'pip-compile  {extra_index_string}  requirements/requirements.in')

#
# @task
# def req_upgrade(ctx):
#     '''
#     Compile Python requirements with upgrading.
#     '''
#     extra_index_string = _get_extra_indexes_string()
#     ctx.run(
#         f'pip-compile -U {extra_index_string} requirements/requirements.in')


@task
def build(ctx):
    '''
    Install all dependencies.
    '''
    ctx.run('pip3 install -r requirements/requirements.txt')


@task
def rebuild(ctx):
    '''
    Compile and rebuild the environment dependencies
    '''
    ctx.run('inv req-compile && inv build')

#
# @task
# def run(ctx, env='development', local=False):
#     '''
#     Runs Dash Server
#     '''
#     default_port = 8000
#     port = os.environ.get('PORT', default_port)
#     if not local:
#         ctx.run(
#             f"doppler run --config={env} --command=\"gunicorn -b :{port} --timeout=1800 --workers=4 main:server\"")
#     else:
#         ctx.run(
#             f"doppler run --config={env}_local --command=\"python main.py\"")
