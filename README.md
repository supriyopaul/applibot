**About "Applibot"**
Applibot is crafted with **Retrieval Augmented Generation (RAG)** at its heart, serving as a guiding companion in the job-seeking saga. More than a mere application aid, Applibot is your strategic partner, designed to streamline the complexities of job hunting across all professions.

The essence of Applibot lies in its ability to smarten your professional footprint. It neatly organizes your resumes, dresses your information in polished templates, and helps articulate cover letters that capture your unique voice. Beyond mere document management, Applibot draws upon your own experiences to provide nuanced responses to inquiries, direct messages, and personalized expressions of interest that align with the roles you aspire to fill.

With an analytical feature that maps your abilities against job requirements, Applibot provides a mirror to reflect your fit for a position, guiding you to fine-tune your presentations to prospective employers.

Security and simplicity are pillars of the Applibot experience, ensuring peace of mind and a straightforward, user-friendly interface. Whether you're a seasoned professional or just starting out, Applibot is here to support your journey to the next opportunity. Let's take the leap into your future career together. 🚀

**Note**: To fully harness the capabilities of Applibot, particularly the ones that interact with the GPT-4 model, you'll need an OpenAI API key that can access GPT-4. As of now, the GPT-4 access is a premium feature. Ensure you possess the necessary permissions.

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

To install and set up the application, you can either use a virtual environment or Docker:

### Virtual Environment Setup:

1. **Create a virtual environment and activate it**:
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

Before running the application, you will need to set up your configuration file. You can start by copying the sample configuration and modifying it to suit your needs.

1. **Copy the sample configuration file**:
    ```bash
    cp sample-server-config.yaml my-config-file.yaml
    ```

2. **Edit the configuration file**:
    ```bash
    nano my-config-file.yaml
    ```

***Important*:** Ensure that your** OpenAI API key** (`chat-model.key` and `embeddings-model.key`) is correctly configured and has access to the required models and services, as the GPT-4 model is a paid service and requires proper authentication and authorization.

   Save and exit the editor.

## Run

Depending on your installation method, choose the appropriate run command:

### For Virtual Environment:

```bash
python -m applibot.server --config my-config-file.yaml
```

This will start the application, making it accessible on the specified host and port in your configuration file (default is `0.0.0.0:9000`).

### For Docker:

Ensure that the path to your configuration file is correctly mapped:

```bash
docker run \
    -p 9000:9000 \
    -v $(pwd)/my-config-file.yaml:/usr/src/app/my-config-file.yaml \
    -v $(pwd)/my-data/:/usr/src/app/my-data/ \
    applibot:latest
```

The Docker container will start, and the application will be accessible on the host's port `9000`.


## Postgres setup
```
docker run -itd -e POSTGRES_USER=applibot_user -e POSTGRES_PASSWORD=change_this_password -p 5432:5432 -v ./my-data/postgresql:/var/lib/postgresql/data --name postgresql postgres
```
