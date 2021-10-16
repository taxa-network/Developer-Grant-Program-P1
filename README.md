# Steps to complete the Taxa SDK challenge

## Preparation

Submit your Github username to the tService with AppID (code hash) `QmVo7WE5P1LK44a7qwt3fnozULqDRrDF4s9bQejPGwTq8o`:

```py
import json

@taxa.route("/register")
def register():
    data = json.loads(request.data)
    username = data['github_name']

    if 'registrations' not in session:
        session['registrations'] = set()

    session['registrations'].add(username)

@taxa.route("/get_registrations")
@taxa.authorize_only(certs=['M9htC3nNBVqnVI5NXrHESGDZtiWtk44c95BL2y2xVb80YN73Px/o71b3b61D8BpipAMdigUJ4uyZgLLZeHi2yw=='])
def get_registrations():
    response.add(' '.join(session['registrations']))
    session['registrations'] = set()
```

This tService contains 2 entry functions: 

`"/register"` Takes the github_name as the input from you, temporary stores the names inside a session object. The names are secured by Intel SGX's "sealing" mechanism, and inacccessible even to the node operator.

`"/get_registrations"` Is a limited-access entry that only opens to the Taxa Team. We will use this function to read the names of those who participate in the Taxa Developer Grant Program.

To complete the challenge, you need to:

* Setup the SDK.
* Craft a tService request to the `/register` function, put your Github username in the "github_name" field of the request.
* Connect to Taxa Network and send the tService request.


## Steps

1. Install the Taxa Network Python SDK:
	```
	sudo pip install taxa_sdk
	```

2. Setup your Intel SPID/PRIMARY_KEY: As an independent developer, you need the **service provider ID (SPID)** and **primary key** in order to initialize an attestation with SGX environments.

	1. Register with Intel [here](https://software.intel.com/registration/?lang=en-us)
	2. Go to [https://api.portal.trustedservices.intel.com/EPID-attestation ](https://api.portal.trustedservices.intel.com/EPID-attestation)

	In the Development access section, click the **Subscribe (unlickable)** button. Follow the steps to generate your SPID and Primary Key.
	![Get SPID step 1](https://user-images.githubusercontent.com/32873616/137424403-26fd5e10-9471-4c1a-b590-c7c9f2a3c250.png)
	Edit the SDK's configurationn file `taxa_sdk/bin/taxaclient.ini`, fill in the SPID and Primary Key you applied for in the previous step.
	![Get SPID step 2](https://user-images.githubusercontent.com/32873616/137424606-ed3ed8c0-b415-40a9-9769-b985d512985e.png)


	```ini
	[IAS]
	SPID = YOUR_SPID_HERE
	PRIMARY_KEY = YOUR_PRIMARY_KEY_HERE

	[NETWORK]
	TAXA_SERVER_HOST = localhost
	TAXA_SERVER_PORT = 22222
	TAXA_SERVER_CERT_PATH = ./sp_server.crt
	```

3. Create a new file for the tService (i.e. "tService.py"), and put inside [the code](tService.py) with hash QmVo7WE5P1LK44a7qwt3fnozULqDRrDF4s9bQejPGwTq8o .

	> Please note: The tService code must be EXACTLY the same as that in the `tService.py`. Any change to the code file (including space/newlines/comment) will change the code's hash and AppID. A request with the wrong AppID will still be processed by Taxa Network, but won't be tracked and recorded for the purpose of the Taxa Developer Grant Program.

4. Create a client file called "dev_program.py", import the Taxa SDK to craft and send the request.

	Sample code:

	```py
	from taxa_sdk import TaxaRequest

	req = TaxaRequest(
	    "taxa_developer_program.json",
	    verbose=True,
	    peer_cert_b64="smDymzFdUKqPttOwpaXk9lGx4enzKmi33BEIBAfVzWX+iQbRQnJm6kPBUbSf8dz3m4Yg1nbJ2LkJGdUxK0xWhQ=="
	)
	req.send(
	  data={'github_name': "[github_username]"},
	  function="register",
	  code_path="/path/to/dev_program_code.py"
	)
	```

	Replace "[github_username]" with your Github username that has been verified during the registration. On the last line, put the path to the first file you made.
5. Send the request by running "dev_program.py" on the command line:

	```
	python3 dev_program.py
	```

6. A successful submission will result in a response with `response-code: 1000`. For example:
	```JSON
	{"status":200,"response":"{'version': '0.1', 'pyxa-version': '0.1', 'response-code': '1000', 'direction': '0', 'session-size-remaining': 8155, 'session-usage': '0.44%', 'content-type': 'text/plain', 'content-transfer-encoding': 'base64', 'data': 'i9u2c5LHA53OuXg3iI0ijQ==\\n', 'public-message': ''}\n"}
	```

	Here we are running a cronjob to query from the privileged function `"/get_registrations"` to read your Github usernames. It takes up to 5 minutes to add your github username into the finalist list.

	To check if you have passed the challenge: 

	1. Join Taxa Network's [Discord](https://discord.com/invite/BusRMXf). Go to the [#developer-grant-program-result](https://discord.com/channels/610854636785762369/887851169005858826) channel.
	2. Type a message `/check [github_username]`. And our Discord bot will automatically reply to you!

	![Check result](https://user-images.githubusercontent.com/32873616/137426630-1965d4ff-b84e-4ca2-8451-a4a5b6c54cb7.png)
