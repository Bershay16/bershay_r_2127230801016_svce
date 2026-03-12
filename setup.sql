-- psql -U postgres -h 127.0.0.1 -p 5433 -c "CREATE DATABASE securin_nvd;"
-- psql -U postgres -h 127.0.0.1 -p 5433 -d securin_nvd -f setup.sql

CREATE TABLE IF NOT EXISTS cpes (
    id                      BIGSERIAL PRIMARY KEY,
    cpe_title               VARCHAR(512),
    cpe_22_uri              TEXT,
    cpe_23_uri              TEXT,
    reference_links         TEXT[],
    cpe_22_deprecation_date DATE,
    cpe_23_deprecation_date DATE
);

CREATE INDEX IF NOT EXISTS ix_cpes_cpe_title       ON cpes (cpe_title);
CREATE INDEX IF NOT EXISTS ix_cpes_cpe_22_uri      ON cpes (cpe_22_uri);
CREATE INDEX IF NOT EXISTS ix_cpes_cpe_23_uri      ON cpes (cpe_23_uri);
CREATE INDEX IF NOT EXISTS ix_cpes_cpe_22_dep_date ON cpes (cpe_22_deprecation_date);
CREATE INDEX IF NOT EXISTS ix_cpes_cpe_23_dep_date ON cpes (cpe_23_deprecation_date);