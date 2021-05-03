-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################


DROP TABLE IF EXISTS administrative_division_zsj;
CREATE TABLE administrative_division_zsj
AS SELECT
    zsj.ogc_fid ogc_fid_zsj,
	zsj.gml_id gml_id_zsj,
	zsj.kod gid,
    zsj.nazev nazev_zsj,
    zsj.katastralniuzemikod kod_ku,
    administrative_division_ku.nazev_ku,
	administrative_division_ku.kod_obec,
	administrative_division_ku.nazev_obec,
	administrative_division_ku.kod_obec_status,
	administrative_division_ku.kod_orp,
	administrative_division_ku.nazev_orp,
	administrative_division_ku.kod_spravniobec_orp,
	administrative_division_ku.nazev_spravniobec_orp,
	administrative_division_ku.kod_pou,
	administrative_division_ku.nazev_pou,
	administrative_division_ku.kod_spravniobec_pou,
	administrative_division_ku.nazev_spravniobec_pou,
	administrative_division_ku.kod_okres,
	administrative_division_ku.nazev_okres,
	administrative_division_ku.kod_vusc,
	administrative_division_ku.nazev_vusc,
	administrative_division_ku.kod_regionsoudrznosti,
	administrative_division_ku.nazev_regionsoudrznosti,
	administrative_division_ku.nuts_2,
	administrative_division_ku.nuts_3,
	administrative_division_ku.nuts_lau_1,
	administrative_division_ku.nuts_lau_2,
	zsj.platiod plati_od,
   	zsj.definicnibod geom_point,
	zsj.originalnihranice geom_polygon
FROM
	zsj
	LEFT OUTER JOIN administrative_division_ku ON (zsj.katastralniuzemikod=administrative_division_ku.gid);

ALTER TABLE administrative_division_zsj ADD PRIMARY KEY (gid);

SELECT UpdateGeometrySRID('public', 'administrative_division_zsj', 'geom_point', 5514);
SELECT UpdateGeometrySRID('public', 'administrative_division_zsj', 'geom_polygon', 5514);

CREATE INDEX administrative_division_zsj_geom_point_idx
    ON public.administrative_division_zsj USING gist (geom_point)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_zsj_geom_polygon_idx
    ON public.administrative_division_zsj USING gist (geom_polygon)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_zsj_nazev_idx
    ON public.administrative_division_zsj USING btree
    (nazev_zsj COLLATE pg_catalog."cs_CZ.utf8" ASC NULLS LAST)
    TABLESPACE pg_default;
