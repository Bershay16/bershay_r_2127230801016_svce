-- PostgreSQL Database

CREATE DATABASE securin_nvd
\c securin_nvd

CREATE TABLE IF NOT EXISTS cpes (
    id                      BIGSERIAL PRIMARY KEY,
    cpe_title               VARCHAR(512),
    cpe_22_uri              TEXT,
    cpe_23_uri              TEXT,
    reference_links         TEXT[],
    cpe_22_deprecation_date DATE,
    cpe_23_deprecation_date DATE
);

CREATE INDEX IF NOT EXISTS ix_cpes_cpe_title ON cpes (cpe_title);