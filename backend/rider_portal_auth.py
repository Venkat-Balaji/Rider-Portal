import time
import requests
from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User

_JWKS_CACHE = {'keys': None, 'fetched_at': 0}
_JWKS_TTL = 60 * 60  # 1 hour

def _get_jwks():
    url = settings.SUPABASE_JWKS_URL
    if not url:
        raise RuntimeError('SUPABASE_JWKS_URL not configured')
    if _JWKS_CACHE['keys'] and time.time() - _JWKS_CACHE['fetched_at'] < _JWKS_TTL:
        return _JWKS_CACHE['keys']
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    _JWKS_CACHE['keys'] = resp.json()
    _JWKS_CACHE['fetched_at'] = time.time()
    return _JWKS_CACHE['keys']

def _get_public_key_for_token(token):
    # Get kid from token header and find matching key
    header = jwt.get_unverified_header(token)
    kid = header.get('kid')
    jwks = _get_jwks()
    keys = jwks.get('keys', [])
    for key in keys:
        if key.get('kid') == kid:
            return key
    # fallback: return jwks (jose can accept jwks)
    return jwks

class SupabaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        token = auth[1].decode()
        try:
            key_or_jwks = _get_public_key_for_token(token)
            payload = jwt.decode(
                token,
                key_or_jwks,
                algorithms=['RS256'],
                audience=getattr(settings, 'SUPABASE_AUDIENCE', None),
                issuer=getattr(settings, 'SUPABASE_ISS', None)
            )
        except Exception as exc:
            raise exceptions.AuthenticationFailed(f'Invalid token: {exc}')
        sub = payload.get('sub')
        email = payload.get('email')
        if not sub:
            raise exceptions.AuthenticationFailed('Token missing sub claim')
        # Map to local user - create minimal record if not exists
        user, created = User.objects.get_or_create(
            supabase_user_id=sub,
            defaults={'email': email or f'{sub}@noemail', 'username': (email.split("@")[0] if email else sub[:8])}
        )
        user._supabase_claims = payload
        return (user, None)
