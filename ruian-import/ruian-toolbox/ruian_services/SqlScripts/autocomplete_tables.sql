-- ##################################################
-- This script creates Auto complete search tables
-- ##################################################

-- --------------------------------------------------
-- Create table psc
-- --------------------------------------------------
DROP TABLE IF EXISTS  ac_psc;
CREATE TABLE ac_psc
AS
SELECT CAST(psc AS text), nazev_obce, nazev_casti_obce, nazev_ulice
FROM address_points
GROUP BY psc, nazev_obce, nazev_casti_obce, nazev_ulice;

-- --------------------------------------------------
-- Create table address_points
-- --------------------------------------------------
DROP TABLE IF EXISTS ac_obce;
CREATE TABLE ac_obce
AS SELECT nazev_obce
FROM address_points
GROUP BY nazev_obce
ORDER BY nazev_obce;

-- --------------------------------------------------
-- Create table ac_ulice
-- --------------------------------------------------
DROP TABLE IF EXISTS ac_ulice;
CREATE TABLE ac_ulice
AS
SELECT nazev_ulice, nazev_obce, nazev_casti_obce, CAST(psc AS text)
FROM address_points
WHERE nazev_ulice <> ''
GROUP BY nazev_ulice, nazev_obce, nazev_casti_obce, psc
ORDER BY nazev_ulice, nazev_obce, nazev_casti_obce, psc;

-- --------------------------------------------------
-- Create table ac_casti_obce
-- --------------------------------------------------
DROP TABLE IF EXISTS ac_casti_obce;
CREATE TABLE ac_casti_obce AS
SELECT nazev_casti_obce, nazev_obce
FROM address_points
GROUP BY nazev_casti_obce, nazev_obce
ORDER BY nazev_casti_obce, nazev_obce;