from fastmcp import FastMCP
from fastmcp.server.auth import require_scopes
from fastmcp.server.auth.providers.jwt import JWTVerifier,RSAKeyPair
from fastmcp.server.dependencies import get_access_token
from starlette.responses import JSONResponse
from starlette.requests import Request 
import hmac # to compae secret keys 

HOST = "127.0.0.1"
PORT = 8004
ISSUER = f"http://{HOST}:{PORT}"   # who created the token
AUDIENCE = "secure-mcp-server"    # for whom the authentuxation is for  
TOKEN_LIFETIME_SECONDS = 3  # token expiry time 

# "aud": which server the token is for
key_pair = RSAKeyPair.generate()  

# public/private keys, access token
REGISTERED_CLIENTS = {
"reader-app": {                    
"secret": "reader-secret",     
# client-id
# client-secret
"allowed_scopes": ["app:read"],
},
"admin-app": {
"secret": "admin-secret",
"allowed_scopes": ["app:read", "db:reset"],
},
}




mcp = FastMCP(
  "Production-style Secure Server",
  auth=JWTVerifier(
  public_key=key_pair.public_key,
  issuer=ISSUER,
  audience=AUDIENCE,
)
)

def error_response(error:str,status_code:int)->JSONResponse:
    """Build and OAUTH error answer"""
    return JSONResponse({"error":error},status_code=status_code)

def is_valid(client:dict|None,client_secret:str)->bool:
    if client is None:
        return False
    hmac.compare_digest(client_secret.encode(),client["secret"].encode())


@mcp.tool(auth=require_scopes("app:read"))
def greet(name:str)->str:
    """Return a Greetful message to a given name """
    return f"Hello {name}, How are you?"


@mcp.tool(auth=require_scopes("app:read"))
def whoami()->str:
    """Tell the caller who they think they are , and what they may do"""
    token=get_access_token()
    return f"I am {token.client_id} and with scopes {token.scopes}"


@mcp.tool(auth=require_scopes("db:reset"))
def reset_database()->str:
    """Reset the database , Dangerous needs the db-reset scope"""
    print("Reset database called")
    return "Database reset done!"


@mcp.custom_route("/token",methods=['POST'])
async def create_token(request:Request)->JSONResponse:
    form = await request.form()
     #1. Check
    if form.get("grant_type") != "client_credentials":
      return error_response("unsupported_grant_type", 400)
    
    #2. Check the client
    client_id = str(form.get("client_id", ""))
    client_secret = str(form.get("client_secret", ""))
    client = REGISTERED_CLIENTS.get(client_id)

    if not is_valid(client, client_secret):
       return error_response("invalid_client", 401)
    
    #3. Check the scope
    requested_scopes = (str(form.get("scope", "")).split() or client["allowed_scopes"])
    for scope in requested_scopes:
     if scope not in client["allowed_scopes"]:
        return error_response("invalid_scope", 400)
     
    access_token = key_pair.create_token(
    subject=client_id,      
    issuer=ISSUER,          
    audience=AUDIENCE,      
    scopes=requested_scopes,               
    expires_in_seconds=TOKEN_LIFETIME_SECONDS)


    return JSONResponse({
    "access_token": access_token,
    "token_type": "Bearer",
    "expires_in": TOKEN_LIFETIME_SECONDS,
    "scope": " ".join(requested_scopes)
    })


if __name__=="__main__":
   mcp.run(transport="http",show_banner=False,host=HOST,port=PORT)