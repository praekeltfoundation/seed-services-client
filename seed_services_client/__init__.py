"""Seed Services client library."""

from .identity_store import IdentityStoreApiClient
from .stage_based_messaging import StageBasedMessagingApiClient
from .auth import AuthApiClient

__version__ = "0.1.0"

__all__ = [
    'IdentityStoreApiClient', 'StageBasedMessagingApiClient', 'AuthApiClient'
]
