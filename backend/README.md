# Flat Finder Backend

## Running the server locally

### Prerequisites

You must have [Python 3](https://www.python.org/downloads/) version 3.11 or newer installed on your system

### Create a virtual environment

**Note**: the following commands work on Linux/MacOS. For Windows the commands
may differ slightly.

Inside this directory, run

```bash
python3 -m venv venv
. venv/bin/activate
```

### Installing dependencies

Inside this directory, run

```bash
pip3 install -r requirements.txt
```

### Setting up Google Cloud OAuth 2.0 Client

We use Google OAuth and OpenID for authentication and authorisation. To get
started, you will need to [set up this API on the Google API Console](https://developers.google.com/identity/openid-connect/openid-connect#appsetup). Follow
the instructions in the preceding link.

A summary of the instructions:

1. Create a new Google project for this application. Wait for it to provision.
   ![](https://user-images.githubusercontent.com/68463406/229338957-09d0506c-10db-4a6e-a372-4fe99456533b.png)
2. Select the newly created project from the list opened in the top left of
   the Google console.
   ![](https://user-images.githubusercontent.com/68463406/229338962-088f0de7-5282-480a-9c8c-bb2c2fc5768e.png)
3. Navigate to the "APIs & Services" page, you can find this by typing in the
   search bar, then go to the credentials tab.
   ![](https://user-images.githubusercontent.com/68463406/229338963-61cc2149-8b79-46ac-94bc-e4aeb3978471.png)
4. Click the "Configure Consent Screen" button and follow the wizard. It is
   sufficient to only fill in the mandatory fields in the "OAuth consent screen"
   step.
5. In the "Scopes" step, click "Add or remove scopes" and select check the
   following scope:
   |Scope|User-facing description|
   |-----|-----------------------|
   |.../auth/userinfo.email|See your primary Google Account email address|

   and scroll down to the update button.
   ![](https://user-images.githubusercontent.com/68463406/229338972-d9f04e10-2a68-4d77-8941-a34d9ee658a6.png)
6. Add some test users (e.g. yourself) that will be able to access the
   application.
   ![](https://user-images.githubusercontent.com/68463406/229338974-3b90505b-fb8c-4d22-a20a-df4b16ca047e.png)
7. Click save and continue and on the "Summary" navigate back to the
   "Credentials" tab.
8. Now you want to actually create an OAuth credential to use with the
   application. Navigate to "Create Credentials" and "OAuth client ID" and
   select "Web application" in the dropdown.
   ![](https://user-images.githubusercontent.com/68463406/229338977-bae56550-50f9-4537-b39f-e7d26f4377dc.png)
9.  You need to add "Authorized redirect URIs" for the authentication to work.
   I have found that using `localhost` did not work for me, so instead use
   `127.0.0.1` as your host. Enter the full URL to the authentication endpoint,
   including the protocol and port number.
   ![](https://user-images.githubusercontent.com/68463406/229338979-8e9e1b99-f7a6-4b74-bcc4-0b876f8046ba.png)
10. Click "Create" and copy the Client ID and Client secret.

You will need to set the `GOOGLE_AUTH_CLIENT_ID` and `GOOGLE_AUTH_CLIENT_SECRET`
environment variables with the values you copied from the Google Cloud Console
when you run the application.

### Running the server

Set the following environment variables:

```env
FRONTEND_URL=<frontend-url>
GOOGLE_AUTH_CLIENT_ID=<your-auth-client-id>
GOOGLE_AUTH_CLIENT_SECRET=<your-auth-client-secret>
ZOOPLA_API_KEY=<your-zoopla-api-key>
SUPERUSER_EMAIL=<test-admin-email>
```

Inside this directory, run

```bash
python3 -m flask run
```

Where frontend URL is the URL to the frontend application. If running locally,
set, use `127.0.0.1` instead of `localhost` to get parity between domains and
hence share cookies without extra configuration. This URL will be used to
redirect the user back to the frontend after SSO authentication.

[Instructions to obtain the Zoopla API key](../docs/API-details/APIdetails.md#getting-api-key)

The `SUPERUSER_EMAIL` is the email of the first admin of the system, needed to
make other users admin. Upon registering a user with that email address,
they get admin rights.

You should see output similar to the following:

```txt
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

### Running tests

To run the application tests, run inside this directory:

```bash
python3 -m pytest
```

## Modifying OpenAPI spec

When modifying the [OpenAPI spec for the backends REST API](openapi.yaml), it
is necessary to regenerate the [client code used by the frontend](../client/src/generated/).

To do this, follow the below stops:

1. Ensure you have [node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) installed on your system
2. Navigate to the [`client`](../client/) directory from the root of this repo
3. Run `npm install` to install the required dependencies
4. Run `npm run openapi:gen` and commit the changes to the autogenerated code
