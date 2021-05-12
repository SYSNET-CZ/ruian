-- ##################################################
-- Create extended temporary table fulltext_ext and fill it with partial data
-- ##################################################

CREATE TABLE fulltext_c AS
SELECT gid, concat(nazev_obce, ',', nazev_casti_obce, ',', psc, ',', nazev_ulice, ',', cislo_orientacni, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce <> nazev_casti_obce)
	AND (nazev_ulice IS NOT NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NOT NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
-- 363817

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', nazev_casti_obce, ',', psc, ',', nazev_ulice, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce <> nazev_casti_obce)
	AND (nazev_ulice IS NOT NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
-- 651627

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', nazev_casti_obce, ',', psc, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce <> nazev_casti_obce)
	AND (nazev_ulice IS NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
-- 1148929

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', psc, ',', nazev_ulice, ',', cislo_orientacni, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce = nazev_casti_obce)
	AND (nazev_ulice IS NOT NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NOT NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
--1311630

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', psc, ',', nazev_ulice, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce = nazev_casti_obce)
	AND (nazev_ulice IS NOT NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
--2023888

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', psc, ',', cislo_domovni) searchstr
FROM address_points
WHERE (nazev_obce = nazev_casti_obce)
	AND (nazev_ulice IS NULL)
	AND (cislo_domovni IS NOT NULL)
	AND (cislo_orientacni IS NULL)
	AND (psc IS NOT NULL)
ORDER BY searchstr ASC;
--2952923

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr
FROM address_points
WHERE nazev_obce <> nazev_casti_obce;
--4101852

INSERT INTO fulltext_c
SELECT gid, concat(nazev_obce, ',', nazev_ulice) searchstr
FROM address_points
WHERE nazev_obce = nazev_casti_obce;
--5905846

CREATE TABLE fulltext_ext AS
SELECT searchstr, array_agg(gid) gids
FROM fulltext_c
GROUP BY searchstr
ORDER BY searchstr ASC;
--2936900

DROP TABLE fulltext_c;

CREATE INDEX fulltext_ext_searchstr_idx
    ON public.fulltext_ext USING btree
    (searchstr COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;
