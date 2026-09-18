# Security Policy

## Present support boundary

Source Integrity Toolkit is in Phase 1 scaffold development. No production release or implemented audit functionality is available. No version is certified for processing private, hostile or high-consequence evidence. Native filesystem protections, resource guards, parsing and report controls are specified but not implemented or security-tested at P1-W01.

The documents in [PRIVACY_AND_DATA_HANDLING.md](PRIVACY_AND_DATA_HANDLING.md) and [SOURCE_INTEGRITY_THREAT_MODEL.md](SOURCE_INTEGRITY_THREAT_MODEL.md) define future obligations. Their presence is not evidence that runtime protection already exists. Supported interpreter/platform claims require the corresponding later tests.

## Reporting a concern

The verified public reporting route is this repository's [Issues page](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/issues). Use it only for non-sensitive reports or a brief request for a confidential reporting route.

At this work unit, a dedicated private vulnerability-reporting route has **not been verified**. No security email, encryption key or private intake service is advertised. Do not assume that GitHub's private reporting feature is enabled for this repository. Do not submit confidential material through a public issue, PR, comment or attachment.

For a sensitive concern, post only a generic request such as “Please provide a verified private channel for a security report.” Wait for the maintainer to identify and verify a suitable route before sharing details. Omit exploit instructions, credentials, private URLs, personal information, identity mappings and real user evidence from that public request. No response deadline, bounty or guaranteed confidential channel is promised.

A non-sensitive report can identify the affected commit and file, the violated requirement, the expected behavior and a minimal fictional reproducer. Clearly distinguish an observed result from a concern about a proposed implementation. Do not test against third-party systems or use real protected data to demonstrate a defect.

## Handling and scope

Maintainers should preserve the finding and its evidence, identify the affected specification and stop unsafe work. A fix to a frozen specification needs explicit scoped authorization and a recorded amendment. A later implementation fix must retain regression evidence without exposing confidential reproductions.

This repository does not operate a public audit service or collect user evidence. If sensitive information is accidentally published, stop further sharing and coordinate containment through an appropriate verified channel. Deleting a current file alone does not remove Git history, external copies or cached disclosures.

This policy adds no warranty, legal safe-harbor promise, or downstream restriction to Apache-2.0. It describes the project's present development and reporting boundary.
