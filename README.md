![Apllibot Logo](https://github.com/supriyopaul/applibot/assets/33823698/7b4699fe-e749-44c2-bd69-47b7ad456beb)

# **About "Applibot"**

Applibot is crafted with **Retrieval Augmented Generation (RAG)** at its heart, serving as a guiding companion in the job-seeking saga. More than a mere application aid, Applibot is your strategic partner, designed to streamline the complexities of job hunting across all professions.

The essence of Applibot lies in its ability to smarten your professional footprint. It neatly organizes your resumes, dresses your information in polished templates, and helps articulate cover letters that capture your unique voice. Beyond mere document management, Applibot draws upon your own experiences to provide nuanced responses to inquiries, direct messages, and personalized expressions of interest that align with the roles you aspire to fill.

With an analytical feature that maps your abilities against job requirements, Applibot provides a mirror to reflect your fit for a position, guiding you to fine-tune your presentations to prospective employers.

Security and simplicity are pillars of the Applibot experience, ensuring peace of mind and a straightforward, user-friendly interface. Whether you're a seasoned professional or just starting out, Applibot is here to support your journey to the next opportunity. Let's take the leap into your future career together. 🚀

**Note**: To fully harness the capabilities of Applibot, particularly the ones that interact with the **GPT-4 model**, you'll need an OpenAI API key that can access GPT-4. As of now, **the GPT-4 access is a premium feature**. Ensure you possess the necessary permissions.

**Steps to Obtain an OpenAI API Key:**

1. **Sign Up on OpenAI**: Navigate to the [OpenAI website](https://openai.com/) and create an account.
2. **Verify Your Account**: Confirm your account through the verification link sent to your email.
3. **Login**: Use your credentials to log in to your OpenAI account.
4. **Access API Section**: Click on your account name at the top right and select "View API keys".
5. **Generate a New Key**: Click "Create new secret key", name it appropriately, and then generate.
6. **Copy & Store Your Key**: Securely copy and store this key; it won't be retrievable again.
7. **Billing Setup**: Ensure you have a payment method associated for any API usage charges.
8. **Set Usage Limits**: Control your expenditure by setting monthly API usage limits.

## Installation

Clone the project and navigate to its directory:

```bash
git clone https://github.com/supriyopaul/applibot
cd applibot
```

Choose between a virtual environment or Docker for setup:

### Virtual Environment Setup:

1. **Create and activate a virtual environment**:
    ```bash
    python3.9 -m venv ./venv
    source venv/bin/activate
    ```

2. **Install the application**:
    ```bash
    pip install .
    ```

### Docker Setup:

1. **Build the Docker image**:
    ```bash
    docker build -t applibot:latest .
    ```

## Configuration

Set up your configuration file from the provided sample:

1. **Copy the sample configuration file**:
    ```bash
    cp sample-server-config.yaml my-config-file.yaml
    ```

2. **Edit the configuration file**:
    ```bash
    nano my-config-file.yaml
    ```

***Important***: Confirm your OpenAI API key is correctly set:

```bash
$ grep -B 4 "change_this" ./my-config-file.yaml

chat-model:
  model-name: gpt-4-1106-preview
  temperature: 0.0
  key: sk-change_this_default_key
  cache: True

embeddings-model:
  name: OpenAIEmbeddings
  key: sk-change_this_default_key
```

Make sure to replace `change_this_default_key` with your actual API keys.

## DB Setup

Set up a PostgreSQL database for Applibot:

```bash
docker run -itd -e POSTGRES_USER=applibot_user -e POSTGRES_PASSWORD=default_password -p 5432:5432 -v ./my-data/postgresql:/var/lib/postgresql/data --name postgresql postgres
```

***Important***: Update the database URL in the configuration file to match your credentials:

```bash
$ grep -B 4 "postgresql" ./sample-server-config.yaml
  pwd-context-depricated: auto
  
table-store:
  postgres:
    url: "postgresql://applibot_user:default_password@localhost/applibot_db"
```

Replace `applibot_user` and `default_password` with your PostgreSQL credentials.

## Run

Launch Applibot:

### For Virtual Environment:

```bash
python -m applibot.server --config my-config-file.yaml
```

### For Docker:

Map your configuration file path correctly:

```bash
docker run \
    -p 9000:9000 \
    -v $(pwd)/my-config-file.yaml:/usr/src/app/my-config-file.yaml \
    -v $(pwd)/my-data/:/usr/src/app/my-data/ \
    applibot:latest
```

### Accessing the API Documentation
When everything goes fine, you should see:

```
Database does not exist, creating...
Database created.
INFO:     Started server process [86118]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

You can access the API documentation and try out the API using the service host and port specified in your configuration file:

```bash
$ grep -A 4 "service" ./sample-server-config.yaml
service:
  host: 0.0.0.0
  port: 9000
  workers: 1
  data-path: my-data/
```

In this case, the API documentation would be available at: [http://localhost:9000/docs](http://localhost:9000/docs)
