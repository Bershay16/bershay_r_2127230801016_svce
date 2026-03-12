CREATE TABLE IF NOT EXISTS cpes (
    id                      BIGSERIAL PRIMARY KEY,
    cpe_title               VARCHAR(512),
    cpe_22_uri              TEXT,
    cpe_23_uri              TEXT,
    reference_links         TEXT[],
    cpe_22_deprecation_date DATE,
    cpe_23_deprecation_date DATE
);