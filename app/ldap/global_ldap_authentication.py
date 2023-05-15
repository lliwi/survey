from ldap3 import Server, Connection, ALL, SUBTREE, SIMPLE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from flask import current_app

def global_ldap_authentication(user_name, user_pwd):
  
# ldap server hostname and port
    ldap_server = "ldap://"+ current_app.config['LDAP_SERVER'] + ":389"

    # root dn
    root_dn = current_app.config['LDAP_ROOT_DN']
	
    # service account dn and password
    service_dn = current_app.config['LDAP_USER']
    service_password = current_app.config['LDAP_PASSWORD']


    # create server and connection objects
    server = Server(ldap_server)
    conn = Connection(server, user=service_dn, password=service_password, authentication=SIMPLE)

    try:
        # authenticate service account
        conn.bind()

        # search for the user
        search_filter = f"({current_app.config['LDAP_ATTRIBUTE']}={user_name})"
        conn.search(search_base=root_dn, search_filter=search_filter, search_scope=SUBTREE)
        
        # check if the user was found
        if len(conn.entries) == 0:
            return "User not found"

        # construct user_dn using the distinguishedName attribute of the user object
        user_dn = conn.entries[0].entry_dn

        # authenticate user
        user_conn = Connection(server, user=user_dn, password=user_pwd, authentication=SIMPLE)
        user_conn.bind()

        # check if the user authentication is successful
        if not user_conn.bound:
            return "Invalid credentials"

        # authentication successful
        return "Success"

    except LDAPException as e:
        # authentication failed
        return f"LDAP error: {e}"
    