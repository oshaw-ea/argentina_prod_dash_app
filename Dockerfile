FROM python:3.9.23-slim-bookworm

ARG DOPPLER_TOKEN_ARG 
ENV DOPPLER_TOKEN ${DOPPLER_TOKEN_ARG}
ENV ENVIRONMENT ${ENVIRONMENT}
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV GOOGLE_APPLICATION_CREDENTIALS /secrets/gcp_credentials.json

# Install Doppler CLI/GCC/PG
RUN apt update &&\
    apt-get install -y apt-transport-https ca-certificates curl gnupg libpq-dev python3-dev build-essential&& \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | apt-key add - && \
    echo "deb https://packages.doppler.com/public/cli/deb/debian any-version main" | tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update &&\
    apt-get -y install --no-install-recommends doppler&&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /secrets

# Pull GCP credentials from Doppler
RUN echo $(doppler secrets get GCP_SERVICE_ACCOUNT_JSON --plain) | base64 --decode  > gcp_credentials.json

WORKDIR /app

COPY . .

# Install base requirements
RUN python -m pip install --upgrade pip &&\
    pip3 install invoke pip-tools keyrings.google-artifactregistry-auth &&\
    inv build

# Delete GCP Build Secret
RUN rm -rf /secrets

EXPOSE 8000/tcp

ENTRYPOINT ["inv", "run", "--env=$ENVIRONMENT"]