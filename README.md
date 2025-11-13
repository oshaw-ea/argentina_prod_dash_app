# US prod dash app v2

Underlying package: for computations: https://github.com/energyaspects/us_prod_model_v2.git


# Python version:
3.12

```bash
pip install pip-tools invoke keyrings.google-artifactregistry-auth doppler-env uv
```

```bash
uv pip install git+https://github.com/energyaspects/helper_functions.git
```
```bash
uv pip install git+https://github.com/energyaspects/argentina_prod.git
```

Then auth with your GCP account by running:

```bash
gcloud auth application-default login
```

Note: if you don't have gcloud tools installed follow this [doc](https://cloud.google.com/sdk/docs/install) to install it.

### Install project dependencies

```bash
inv build
```

# Setup Doppler project
```bash
doppler setup
```
Select argentina_prod_model
Select dev / prd depending on needs

# Inject secrets in Pycharm
https://docs.doppler.com/docs/pycharm

# Deployed Apps:
