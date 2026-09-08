---
layout: home

hero:
  name: Sombra
  text: Local PII anonymization proxy
  tagline: Masks Brazilian PII — CPF, CEP, CNPJ, names, e-mails, addresses — in real time before it reaches a remote LLM provider.
  image:
    src: /img/sombra.png
    alt: Sombra
  actions:
    - theme: brand
      text: Get started
      link: /getting-started/install
    - theme: alt
      text: Architecture
      link: /concepts/architecture

features:
  - title: Real-time masking
    details: Prompts are intercepted and masked before they ever leave your machine.
  - title: Built for Brazil
    details: Recognizers for CPF, CEP, CNPJ and street addresses on top of Presidio.
  - title: Local-first
    details: Runs in rootless Podman containers. Zero sensitive data persisted remotely.
---