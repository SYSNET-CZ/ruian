-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################

DROP TABLE IF EXISTS administrative_division_ku;

CREATE TABLE adku1
AS SELECT
	katastralniuzemi.ogc_fid ogc_fid_ku,
	katastralniuzemi.gml_id gml_id_ku,
	katastralniuzemi.kod gid,
	katastralniuzemi.nazev nazev_ku,
	katastralniuzemi.obeckod kod_obec,
	katastralniuzemi.platiod plati_od,
	katastralniuzemi.definicnibod geom_point,
	katastralniuzemi.originalnihranice geom_polygon,
	katastralniuzemi.generalizovanehranice geom_polygon_generalized,
	obce.nazev nazev_obec,
	obce.statuskod kod_obec_status,
	obce.okreskod kod_okres,
	obce.poukod kod_pou,
	obce.nutslau nuts_lau_2
FROM
	katastralniuzemi
	LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod);

CREATE TABLE adku2
AS SELECT
	adku1.ogc_fid_ku,
	adku1.gml_id_ku,
	adku1.gid,
	adku1.nazev_ku,
	adku1.kod_obec,
	adku1.nazev_obec,
	adku1.kod_obec_status,
	adku1.kod_okres,
	adku1.kod_pou,
	adku1.nuts_lau_2,
	adku1.plati_od,
	adku1.geom_point,
	adku1.geom_polygon,
	adku1.geom_polygon_generalized,
	okresy.nazev nazev_okres,
	okresy.vusckod kod_vusc,
	okresy.nutslau nuts_lau_1,
	pou.nazev nazev_pou,
	pou.orpkod kod_orp,
	pou.spravniobeckod kod_spravniobec_pou
 FROM
	adku1
	LEFT OUTER JOIN okresy ON (adku1.kod_okres=okresy.kod)
	LEFT OUTER JOIN pou ON (adku1.kod_pou=pou.kod);


CREATE TABLE adku3
AS SELECT
	adku2.ogc_fid_ku,
	adku2.gml_id_ku,
	adku2.gid,
	adku2.nazev_ku,
	adku2.kod_obec,
	adku2.nazev_obec,
	adku2.kod_obec_status,
	adku2.kod_okres,
	adku2.kod_pou,
	adku2.nazev_okres,
	adku2.kod_vusc,
	adku2.nuts_lau_1,
	adku2.nuts_lau_2,
	adku2.nazev_pou,
	adku2.kod_orp,
	adku2.kod_spravniobec_pou,
	adku2.plati_od,
	adku2.geom_point,
	adku2.geom_polygon,
	adku2.geom_polygon_generalized,
	vusc.nazev nazev_vusc,
	vusc.regionsoudrznostikod kod_regionsoudrznosti,
	vusc.nutslau nuts_3,
	orp.nazev nazev_orp,
	orp.spravniobeckod kod_spravniobec_orp,
	obce.nazev nazev_spravniobec_pou
FROM
	adku2
	LEFT OUTER JOIN vusc ON (adku2.kod_vusc=vusc.kod)
	LEFT OUTER JOIN orp ON (adku2.kod_orp=orp.kod)
	LEFT OUTER JOIN obce ON (adku2.kod_spravniobec_pou=obce.kod);

CREATE TABLE administrative_division_ku
AS SELECT
	adku3.ogc_fid_ku,
	adku3.gml_id_ku,
	adku3.gid,
	adku3.nazev_ku,
	adku3.kod_obec,
	adku3.nazev_obec,
	adku3.kod_obec_status,
	adku3.kod_orp,
	adku3.nazev_orp,
	adku3.kod_spravniobec_orp,
	obce.nazev nazev_spravniobec_orp,
	adku3.kod_pou,
	adku3.nazev_pou,
	adku3.kod_spravniobec_pou,
	adku3.nazev_spravniobec_pou,
	adku3.kod_okres,
	adku3.nazev_okres,
	adku3.kod_vusc,
	adku3.nazev_vusc,
	adku3.kod_regionsoudrznosti,
	regionysoudrznosti.nazev nazev_regionsoudrznosti,
	regionysoudrznosti.nutslau nuts_2,
	adku3.nuts_3,
	adku3.nuts_lau_1,
	adku3.nuts_lau_2,
	adku3.plati_od,
	adku3.geom_point,
	adku3.geom_polygon,
	adku3.geom_polygon_generalized
FROM
	adku3
	LEFT OUTER JOIN regionysoudrznosti ON (adku3.kod_regionsoudrznosti=regionysoudrznosti.kod)
	LEFT OUTER JOIN obce ON (adku3.kod_spravniobec_orp=obce.kod);

DROP TABLE IF EXISTS adku1;
DROP TABLE IF EXISTS adku2;
DROP TABLE IF EXISTS adku3;

ALTER TABLE administrative_division_ku ADD PRIMARY KEY (gid);

SELECT UpdateGeometrySRID('public', 'administrative_division_ku', 'geom_point', 5514);
SELECT UpdateGeometrySRID('public', 'administrative_division_ku', 'geom_polygon', 5514);
SELECT UpdateGeometrySRID('public', 'administrative_division_ku', 'geom_polygon_generalized', 5514);

CREATE INDEX administrative_division_ku_geom_point_idx
    ON public.administrative_division_ku USING gist (geom_point)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_geom_polygon_idx
    ON public.administrative_division_ku USING gist (geom_polygon)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_geom_polygon_generalized_idx
    ON public.administrative_division_ku USING gist (geom_polygon_generalized)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_nazev_idx
    ON public.administrative_division_ku USING btree
    (nazev_ku COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;





















DROP TABLE IF EXISTS administrative_division_ku;

CREATE TABLE adku1
AS SELECT
	katastralniuzemi.ogc_fid ogc_fid_ku,
	katastralniuzemi.gml_id gml_id_ku,
	katastralniuzemi.kod gid,
	katastralniuzemi.nazev nazev_ku,
	katastralniuzemi.obeckod kod_obec,
	katastralniuzemi.platiod plati_od,
	katastralniuzemi.originalnihranice geom,
	obce.nazev nazev_obec,
	obce.statuskod kod_obec_status,
	obce.okreskod kod_okres,
	obce.poukod kod_pou
FROM
	katastralniuzemi
	LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod);





CREATE TABLE administrative_division_ku
AS SELECT DISTINCT
	katastralniuzemi.ogc_fid ogc_fid_ku,
	katastralniuzemi.gml_id gml_id_ku,
	katastralniuzemi.kod gid,
	katastralniuzemi.nazev nazev_ku,
	katastralniuzemi.obeckod kod_obec,
	obce.nazev nazev_obec,
	obce.statuskod kod_obec_status,
	obce.okreskod kod_okres,
	obce.poukod kod_pou,
	okresy.nazev nazev_okres,
	okresy.krajkod kod_kraj,
	okresy.vusckod kod_vusc,
	pou.nazev nazev_pou,
	pou.orpkod kod_orp,
	kraje.nazev nazev_kraj,
	kraje.statkod kod_stat,
	vusc.nazev nazev_vusc,
	vusc.regionsoudrznostikod kod_nuts2,
	vusc.nutslau nuts_3,
	orp.nazev nazev_orp,
	staty.nazev nazev_stat,
	staty.nutslau nuts_1,
	regionysoudrznosti.nazev nazev_nuts2,
	regionysoudrznosti.nutslau nuts_2,
	katastralniuzemi.platiod plati_od,
	katastralniuzemi.originalnihranice geom
FROM
	katastralniuzemi
	LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod)
	LEFT OUTER JOIN okresy ON (obce.okreskod=okresy.kod)
	LEFT OUTER JOIN pou ON (obce.poukod=pou.kod)
	LEFT OUTER JOIN kraje ON (okresy.krajkod=kraje.kod)
	LEFT OUTER JOIN vusc ON (okresy.vusckod=vusc.kod)
	LEFT OUTER JOIN orp ON (pou.orpkod=orp.kod)
	LEFT OUTER JOIN staty ON (kraje.statkod=staty.kod)
	LEFT OUTER JOIN regionysoudrznosti ON (vusc.regionsoudrznostikod=regionysoudrznosti.kod);

ALTER TABLE administrative_division_ku ADD PRIMARY KEY (ogc_fid_ku);

SELECT UpdateGeometrySRID('public', 'administrative_division_ku', 'geom', 5514);

CREATE INDEX administrative_division_ku_geom_idx
    ON public.administrative_division_ku USING gist (geom)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_nazev_idx
    ON public.administrative_division_ku USING btree
    (nazev_ku COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_gid_idx
    ON public.administrative_division_ku USING btree
    (gid ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_ku_gml_idx
    ON public.administrative_division_ku USING btree
    (gml_id_ku COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;




