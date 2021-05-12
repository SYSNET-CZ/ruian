-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################


DROP TABLE IF EXISTS administrative_division_zsj;
CREATE TABLE administrative_division_zsj
AS SELECT DISTINCT
    zsj.ogc_fid ogc_fid_zsj,
	zsj.gml_id gml_id_zsj,
	zsj.kod gid,
    zsj.nazev nazev_zsj,
    zsj.katastralniuzemikod kod_ku,
	zsj.platiod plati_od,
	zsj.originalnihranice geom,
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
	regionysoudrznosti.nutslau nuts_2
FROM
	zsj
	LEFT OUTER JOIN katastralniuzemi ON (zsj.katastralniuzemikod=katastralniuzemi.kod)
	LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod)
	LEFT OUTER JOIN okresy ON (obce.okreskod=okresy.kod)
	LEFT OUTER JOIN pou ON (obce.poukod=pou.kod)
	LEFT OUTER JOIN kraje ON (okresy.krajkod=kraje.kod)
	LEFT OUTER JOIN vusc ON (okresy.vusckod=vusc.kod)
	LEFT OUTER JOIN orp ON (pou.orpkod=orp.kod)
	LEFT OUTER JOIN staty ON (kraje.statkod=staty.kod)
	LEFT OUTER JOIN regionysoudrznosti ON (vusc.regionsoudrznostikod=regionysoudrznosti.kod);

ALTER TABLE administrative_division_zsj ADD PRIMARY KEY (ogc_fid_zsj);

SELECT UpdateGeometrySRID('public', 'administrative_division_zsj', 'geom', 5514);

CREATE INDEX administrative_division_zsj_geom_idx
    ON public.administrative_division_zsj USING gist (geom)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_zsj_nazev_idx
    ON public.administrative_division_zsj USING btree
    (nazev_zsj COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_zsj_gid_idx
    ON public.administrative_division_zsj USING btree
    (gid ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_zsj_gml_idx
    ON public.administrative_division_zsj USING btree
    (gml_id_zsj COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;

