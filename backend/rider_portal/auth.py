from jose import jwt
import requests, time
from django.conf import settings
from rest_framework import authentication, exceptions

JWKS_CACHE = {'keys': None, 'fetched_at': 0}
JWKS_TTL = 60 * 60  # 1 hour

def get_jwks():
    if JWKS_CACHE['keys'] and time.time() - JWKS_CACHE['fetched_at'] < JWKS_TTL:
        return JWKS_CACHE['keys']
    resp = requests.get(settings.SUPABASE_JWKS_URL, timeout=5)
    resp.raise_for_status()
    JWKS_CACHE['keys'] = resp.json()
    JWKS_CACHE['fetched_at'] = time.time()
    return JWKS_CACHE['keys']

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        token = auth[1].decode()
        jwks = get_jwks()
        try:
            # use jose.jwt.decode with jwks
            payload = jwt.decode(token, jwks, algorithms=['RS256'], audience=settings.SUPABASE_AUDIENCE, issuer=settings.SUPABASE_ISS)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid token')

        supabase_user_id = payload.get('sub')
        email = payload.get('email')
        # optionally role claim
        role = payload.get('role') or payload.get('app_role')

        # Map or create local user
        from users.models import User
        try:
            user = User.objects.get(supabase_user_id=supabase_user_id)
            # update basic info from token if needed
        except User.DoesNotExist:
            # Optionally auto-create minimal local user entry
            user = User.objects.create(
                supabase_user_id = supabase_user_id,
                email = email,
                username = email.split('@')[0],
            )
        # attach token payload if useful
        user._supabase_claims = payload
        return (user, None)
