-- ##################################################
-- Create temporary table fulltext_a and fill it with partial data
-- ##################################################

DROP TABLE IF EXISTS fulltext_a;
CREATE TABLE fulltext_a AS
SELECT gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr FROM address_points
WHERE nazev_obce <> nazev_casti_obce;

-- --------------------------------------------------
-- add rest of values
-- --------------------------------------------------
INSERT INTO fulltext_a
SELECT gid, concat(nazev_obce, ',', nazev_ulice) searchstr
FROM address_points
WHERE nazev_obce = nazev_casti_obce;

-- --------------------------------------------------
-- Create table fulltext
-- --------------------------------------------------
DROP TABLE IF EXISTS fulltext;
CREATE TABLE fulltext
AS
SELECT searchstr, array_agg(gid) gids
FROM fulltext_a
GROUP BY searchstr;

-- --------------------------------------------------
-- Drop temporary table fulltext_a
-- --------------------------------------------------
DROP TABLE fulltext_a;

-- Index: fulltext_searchstr_idx

-- DROP INDEX public.fulltext_searchstr_idx;

CREATE INDEX fulltext_searchstr_idx
    ON public.fulltext USING btree
    (searchstr COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;
