OPTIONS (SKIP=1)
LOAD DATA
REPLACE
INTO TABLE hosts
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    id,
    name,
    is_superhost,
    created_at "TO_TIMESTAMP(:created_at, 'YYYY-MM-DD HH24:MI:SS')",
    updated_at "TO_TIMESTAMP(:updated_at, 'YYYY-MM-DD HH24:MI:SS')"
)
