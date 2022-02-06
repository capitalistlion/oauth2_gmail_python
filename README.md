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

![oath2_1](https://user-images.githubusercontent.com/29549103/152693982-8445baee-f90c-4e0b-91d7-c9535caf26c6.jpg)

![oath2_2](https://user-images.githubusercontent.com/29549103/152694008-edf13d30-dcd6-496f-8874-44814bea2c67.png)

![oath2_3](https://user-images.githubusercontent.com/29549103/152694012-6087813b-4676-4bcd-ba7a-2a115e5152c4.png)

9. Replace the AUTHORIZATION_CODE variable from 'code' in the redirected url

![oath2_4](https://user-images.githubusercontent.com/29549103/152694025-82facf4a-3498-4b69-89fc-579a13acad97.png)


```python
AUTHORIZATION_CODE = ""
```

10. Run the app again and select the remaining 2 options

```bash
python app.py
```

![oath2_5](https://user-images.githubusercontent.com/29549103/152694032-13a67282-b4c2-48a9-8869-466bfed937df.png)
