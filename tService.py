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
