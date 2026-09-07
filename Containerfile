# Sombra — Presidio Analyzer image
#
# Extends the official Presidio analyzer with Brazilian PII detection:
#   * downloads the Portuguese spaCy model (pt_core_news_lg) for PERSON and
#     LOCATION detection;
#   * loads a recognizer registry that keeps every default recognizer and
#     adds the Sombra Brazilian entities (SOMBRA_CPF, SOMBRA_CEP,
#     SOMBRA_CNPJ, SOMBRA_ADDRESS);
#   * switches the NLP configuration to the Portuguese model.
#
# The analyzer server (app.py in the base image) reads the
# RECOGNIZER_REGISTRY_CONF_FILE and NLP_CONF_FILE environment variables, so
# no code changes are required.

FROM mcr.microsoft.com/presidio-analyzer:latest

# Portuguese spaCy model for PERSON and LOCATION detection
RUN python -m spacy download pt_core_news_lg

# Sombra recognizer registry: default recognizers + Brazilian entities
COPY containers/sombra_recognizers.yaml /presidio/sombra_recognizers.yaml

# spaCy NLP configuration using the Portuguese model
COPY containers/nlp_pt.yaml /presidio/nlp_pt.yaml

# Analyzer engine configuration supporting Portuguese
COPY containers/analyzer_pt.yaml /presidio/analyzer_pt.yaml

# Point the analyzer server at the Sombra configuration
ENV RECOGNIZER_REGISTRY_CONF_FILE=/presidio/sombra_recognizers.yaml
ENV NLP_CONF_FILE=/presidio/nlp_pt.yaml
ENV ANALYZER_CONF_FILE=/presidio/analyzer_pt.yaml