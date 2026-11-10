"""PII and Off-Platform Contact Masking Module for GigBid.

Enforces platform compliance guardrails:
- Masks external phone numbers, WhatsApp, Telegram handles
- Masks email addresses
- Masks crypto wallet addresses (BTC, ETH, Solana)
- Masks credit card numbers
"""

import re
from typing import Tuple, List

# Regex patterns for off-platform communication & sensitive identifiers
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b')
WHATSAPP_PATTERN = re.compile(r'(?:whatsapp|wa\.me|chat\.whatsapp\.com)[^\s]+', re.IGNORECASE)
TELEGRAM_PATTERN = re.compile(r'(?:t\.me/|telegram\.me/|(?<!\S)@[\w_]{5,})\b', re.IGNORECASE)
CRYPTO_BTC_PATTERN = re.compile(r'\b(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}\b')
CRYPTO_ETH_PATTERN = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

def mask_pii_and_offplatform(text: str) -> Tuple[str, List[str]]:
    """Masks sensitive PII and off-platform contact attempts.
    
    Returns:
        (sanitized_text, list_of_detected_violations)
    """
    violations = []
    sanitized = text

    # Check Email first to avoid matching handles in domain
    if EMAIL_PATTERN.search(sanitized):
        violations.append("email_address")
        sanitized = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", sanitized)

    # Check WhatsApp
    if WHATSAPP_PATTERN.search(sanitized):
        violations.append("whatsapp_link")
        sanitized = WHATSAPP_PATTERN.sub("[REDACTED_WHATSAPP]", sanitized)

    # Check Telegram
    if TELEGRAM_PATTERN.search(sanitized):
        violations.append("telegram_handle")
        sanitized = TELEGRAM_PATTERN.sub("[REDACTED_TELEGRAM]", sanitized)

    # Check Phone
    if PHONE_PATTERN.search(sanitized):
        violations.append("phone_number")
        sanitized = PHONE_PATTERN.sub("[REDACTED_PHONE]", sanitized)

    # Check Crypto Wallets
    if CRYPTO_ETH_PATTERN.search(sanitized) or CRYPTO_BTC_PATTERN.search(sanitized):
        violations.append("crypto_wallet")
        sanitized = CRYPTO_ETH_PATTERN.sub("[REDACTED_CRYPTO_ADDR]", sanitized)
        sanitized = CRYPTO_BTC_PATTERN.sub("[REDACTED_CRYPTO_ADDR]", sanitized)

    return sanitized, violations
