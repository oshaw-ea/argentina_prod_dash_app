import os
from invoke import task


ARTIFACT_REGISTRY_LINKS  = [
    'https://europe-west2-python.pkg.dev/ea-analytics-apps/ea-helper-functions/simple/',
    'https://europe-west2-python.pkg.dev/ea-analytics-apps/us-prod-model-v2/simple/',
]

def _get_extra_indexes_string():
    template = '--extra-index-url {link}'
    links = []
    for link in ARTIFACT_REGISTRY_LINKS:
        links.append(template.format(link=link))
    return ' '.join(links)

extra_index_string = _get_extra_indexes_string()


@task
def req_compile(ctx):
    """
    Compile Python requirements without upgrading.
    """
    ctx.run(f'pip-compile {extra_index_string} -v requirements/requirements.in -o requirements/requirements.txt')


@task
def req_upgrade(ctx):
    """
    Compile Python requirements with upgrading.
    """
    ctx.run(f'pip-compile {extra_index_string} -v -U requirements/requirements.in -o requirements/requirements.txt')


@task
def build(ctx):
    """
    Install all dependencies.
    """
    ctx.run(f'pip install {extra_index_string} -r requirements/requirements.txt')


@task
def rebuild(ctx):
    """
    Compile and rebuild the environment dependencies
    """
    ctx.run('inv req-compile && inv build')


@task
def lint(ctx, path='src'):
    """
    Lint project files
    """
    ctx.run(f'pylint --fail-under=9.0 --rcfile=.pylintrc {path}')

@task
def run(ctx, local=True):
    '''
    Runs dash app locally
    '''
    if local:
        ctx.run(
            f"doppler run --command=\"python src/main.py\"")
    else:
        raise NotImplementedError("Production has not been implemented yet.")


@task(
    help={
        'path': 'Specify files or directories to lint',
        'check': 'Only runs check without reformat (default: False)',
    }
)
def lint_black(ctx, path='src', check=False):
    """
    Runs the black formatter.
    """

    cmd = 'black --line-length=100 --skip-string-normalization {check} {path}'.format(
        check='--check' if check else '', path=path
    )
    ctx.run(cmd)
