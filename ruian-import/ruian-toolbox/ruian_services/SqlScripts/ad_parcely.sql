-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################

DROP TABLE IF EXISTS public.administrative_division;
CREATE TABLE public.administrative_division
AS SELECT
    parcely.ogc_fid ogc_fid_parcely,
	parcely.gml_id gml_id_parcely,
	parcely.id gid,
	parcely.kmenovecislo cislo_parc,
	parcely.pododdelenicisla cislo_parc_2,
	parcely.vymeraparcely vymera,
	parcely.katastralniuzemikod kod_ku,
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
   	parcely.platiod plati_od,
	parcely.definicnibod geom_point,
	parcely.originalnihranice geom_polygon,
    parcely.originalnihraniceompv geom_polygon_ompv
FROM
	public.parcely
	LEFT OUTER JOIN administrative_division_ku ON (parcely.katastralniuzemikod=administrative_division_ku.gid);

ALTER TABLE public.administrative_division ADD PRIMARY KEY (gid);

SELECT UpdateGeometrySRID('public', 'administrative_division', 'geom_point', 5514);
SELECT UpdateGeometrySRID('public', 'administrative_division', 'geom_polygon', 5514);
SELECT UpdateGeometrySRID('public', 'administrative_division', 'geom_polygon_ompv', 5514);


CREATE INDEX administrative_division_geom_point_idx
    ON public.administrative_division USING gist (geom_point)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_geom_polygon_idx
    ON public.administrative_division USING gist (geom_polygon)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_geom_polygon_ompv_idx
    ON public.administrative_division USING gist (geom_polygon_ompv)
    TABLESPACE pg_default;

CREATE INDEX administrative_division_cislo_idx
    ON public.administrative_division USING btree
    (cislo_parc ASC NULLS LAST, cislo_parc_2 ASC NULLS LAST)
    TABLESPACE pg_default;
