from __future__ import annotations

from typing import Tuple


VULNERABLE_SIGNATURES = {
    "RSA", "RSA-PSS", "RSASSA-PKCS1", "ECDSA", "DSA", "ED25519", "ED448"
}
VULNERABLE_KEY_EXCHANGE = {
    "RSA-KEX", "RSA", "DH", "DIFFIE-HELLMAN", "ECDH", "ECDHE"
}
LEGACY_SYMMETRIC = {"3DES", "DES", "RC4", "MD5", "SHA-1"}
SAFE_SYMMETRIC = {"AES", "AES-GCM", "CHACHA20-POLY1305", "SHA-256", "SHA-384", "SHA-512"}


ALIASES = {
    "RSA-2048": "RSA",
    "RSA-3072": "RSA",
    "RSA-4096": "RSA",
    "sha256WithRSAEncryption": "RSA",
    "id-ecPublicKey": "ECDSA",
    "ecPublicKey": "ECDSA",
    "ECDHE-RSA": "ECDHE",
    "ECDHE-ECDSA": "ECDHE",
    "DiffieHellman": "DIFFIE-HELLMAN",
    "Ed25519": "ED25519",
    "Ed448": "ED448",
}


def canonicalize_algorithm(name: str, primitive: str = "") -> str:
    if not name:
        return ""
    cleaned = name.strip().upper()
    for key, value in ALIASES.items():
        if cleaned == key.upper():
            return value
    for family in sorted(VULNERABLE_SIGNATURES | VULNERABLE_KEY_EXCHANGE | LEGACY_SYMMETRIC | SAFE_SYMMETRIC, key=len, reverse=True):
        if family in cleaned:
            return family
    if "ECDH" in cleaned:
        return "ECDH"
    if "ECDSA" in cleaned:
        return "ECDSA"
    if "RSA" in cleaned:
        return "RSA"
    if "SHA-1" in cleaned or cleaned == "SHA1":
        return "SHA-1"
    if "SHA-256" in cleaned:
        return "SHA-256"
    return cleaned


def classify_posture(algorithm_family: str, primitive: str = "") -> Tuple[str, str, str]:
    algo = canonicalize_algorithm(algorithm_family, primitive)
    prim = (primitive or "").lower()

    if algo in VULNERABLE_KEY_EXCHANGE or (algo == "RSA" and prim in {"kem", "key-establishment", "key-exchange", "tls", "key transport"}):
        return (
            "quantum-vulnerable",
            "Plan migration to ML-KEM or hybrid key establishment",
            "Public-key key establishment based on RSA/DH/ECDH is vulnerable to future cryptanalytically relevant quantum computers.",
        )
    if algo in VULNERABLE_SIGNATURES or (algo == "RSA" and prim in {"signature", "sign", "verify"}):
        return (
            "quantum-vulnerable",
            "Plan migration to ML-DSA or SLH-DSA, potentially via hybrid deployments",
            "Classical public-key signatures are expected to need replacement or hybridization during PQC migration.",
        )
    if algo in LEGACY_SYMMETRIC:
        return (
            "legacy-but-not-pqc-primary",
            "Replace with modern approved primitives and review quantum-related key length margins",
            "This asset is a classical legacy risk and should be modernized as part of broader crypto hygiene.",
        )
    if algo in SAFE_SYMMETRIC:
        return (
            "monitor",
            "Keep under review; confirm key lengths and protocol context",
            "Symmetric cryptography is not the primary PQC migration driver, but still needs lifecycle management.",
        )
    if algo.startswith("ML-KEM") or algo.startswith("ML-DSA") or algo.startswith("SLH-DSA"):
        return (
            "pqc-ready",
            "Validate interoperability, performance, and policy alignment",
            "This asset already references a NIST-standardized post-quantum algorithm family.",
        )
    return (
        "unknown",
        "Review manually and map to a supported algorithm family",
        "The algorithm could not be confidently classified.",
    )
