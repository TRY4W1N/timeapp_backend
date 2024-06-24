import asyncio

import firebase_admin
from firebase_admin import App, auth
from firebase_admin._user_mgt import ProviderUserInfo, UserRecord

from src.application.service.auth.dto import ProviderIdentity, TokenIdentity, UserIdentity
from src.application.service.auth.enum import AuthProviderEnum
from src.application.service.auth.firebase.interface.gateway import FirebaseGateway


class FirebaseError(Exception):
    """"""


class FirebaseGatewayImplement(FirebaseGateway):
    def __init__(self, name: str, secret_path: str) -> None:
        self._name = name
        self._secret_path = secret_path
        self._is_setup = False
        self._app: App | None = None

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def is_setup(self) -> bool:
        return self._is_setup


    def _get_provider_by_data(self, data: list[ProviderUserInfo]) -> ProviderIdentity:
        provider_data_list = data
        if len(provider_data_list) != 1:
            raise FirebaseError(f"Can't processing parse provider data size != 1: size={len(provider_data_list)}")
        provider_data = provider_data_list[0]
        if provider_data.provider_id == "google.com":
            _type = AuthProviderEnum.GOOGLE
        else:
            raise FirebaseError(f"Can't processing parse provider data: unknown provider `{provider_data.provider_id}`")
        return ProviderIdentity(type=_type, data=provider_data._data)

    async def verify_token(self, token: str, check_revoked: bool = True) -> TokenIdentity:
        if not self._is_setup:
            raise FirebaseError("Not setup")
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, auth.verify_id_token, token, self._app, check_revoked)
        provider_block = data.get("firebase")
        if provider_block is None:
            raise FirebaseError(f"Can't processing parse token data (provider block): {data}")
        provider_sign_in = provider_block.get("sign_in_provider")
        if provider_sign_in is None:
            raise FirebaseError(f"Can't processing parse token data (sign_in_provider): {data}")
        provider_data = provider_block.get("identities")
        if provider_data is None:
            raise FirebaseError(f"Can't processing parse token data (provider_data): {data}")
        token_obj = TokenIdentity(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            email_verified=data["email_verified"],
            pic=data["picture"],
            auth_time=data["auth_time"],
            iss=data["iss"],
            aud=data["aud"],
            uid=data["uid"],
            provider=provider_sign_in,
            provider_data=provider_data,
            iat=data["iat"],
            exp=data["exp"],
        )
        return token_obj

    async def get_user(self, id: str) -> UserIdentity:
        if not self._is_setup:
            raise FirebaseError("Not setup")
        loop = asyncio.get_running_loop()
        data: UserRecord = await loop.run_in_executor(None, auth.get_user, id, self._app)
        provider_obj = self._get_provider_by_data(data=data.provider_data)
        user_obj = UserIdentity(
            id=data.uid,  # type: ignore
            name=data.display_name,  # type: ignore
            active=not data.disabled,
            pic=data.photo_url,  # type: ignore
            email=data.email,  # type: ignore
            email_verified=data.email_verified,
            provider=provider_obj,
        )
        return user_obj

    def setup(self) -> None:
        if not self._is_setup:
            credential = firebase_admin.credentials.Certificate(self._secret_path)
            try:
                # That create app in global firebase_admin scope..
                self._app = firebase_admin.initialize_app(credential=credential, name=self._name)
            except ValueError:
                self._app = firebase_admin.get_app(name=self.name)
        self._is_setup = True

