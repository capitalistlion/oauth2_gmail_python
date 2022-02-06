# OAUTH2 Gmail Python
Send emails using Gmail and Generate OAUTH2 Tokens in Python

## Requirements

* Gmail & Google Developers/Gcloud Account
* Enable Gmail API and grant Send Email scope in your Google Developers/Gcloud Account
* Python 3
* Pip

## Setup

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the virtual environment

```bash
./venv/scripts/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Replace EMAIL_FROM with your gmail (or other provider's) email address.

```python
    EMAIL_FROM = "youremail@gmail.com"
```

5. Replace the following variables using credentials from your Google Developers/Gcloud Account

```python
REDIRECT_URI = "--------"
CLIENT_ID = "-----------.apps.googleusercontent.com"
CLIENT_SECRET = "---------------"
```

6. Run the app

```bash
python app.py
```

7. Go through each option starting from #1

```python
Select an option

1. Generate Authorization Code
2. Generate Tokens
3. Send Email
```

8. For Option #1 You will go through the following steps on your browser when it generates a URL



9. Replace the AUTHORIZATION_CODE variable from 'code' in the redirected url

```python
AUTHORIZATION_CODE = ""
```

10. Run the app again and select the remaining 2 options

```bash
python app.py
```
