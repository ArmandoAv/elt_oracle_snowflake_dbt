OPTIONS (SKIP=1)
LOAD DATA
REPLACE
INTO TABLE listings
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    id,
    listing_url,
    name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at "TO_TIMESTAMP(:created_at, 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"')",
    updated_at "TO_TIMESTAMP(:updated_at, 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"')"
)
