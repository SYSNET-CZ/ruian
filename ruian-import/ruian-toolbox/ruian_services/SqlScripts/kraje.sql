--CREATE TABLE ad_kraje AS
-- SELECT
--	public.ad_kraje_defbod.ogc_fid,
--	public.ad_kraje_defbod.gml_id,
--	public.ad_kraje_defbod.kod,
--	public.ad_kraje_defbod.nazev,
--	public.ad_kraje_defbod.nespravny,
--	public.ad_kraje_defbod.statkod,
--	public.ad_kraje_defbod.platiod,
--	public.ad_kraje_defbod.idtransakce,
--	public.ad_kraje_defbod.globalniidnavrhuzmeny,
--	public.ad_kraje_defbod.nutslau,
--	public.ad_kraje_defbod.datumvzniku,
--	public.ad_kraje_defbod.geom definicnibod
-- FROM public.ad_kraje_defbod;

-- CREATE TABLE ad_kraje1 AS
-- SELECT
--	public.ad_kraje.ogc_fid,
--	public.ad_kraje.gml_id,
--	public.ad_kraje.kod,
--	public.ad_kraje.nazev,
--	public.ad_kraje.nespravny,
--	public.ad_kraje.statkod,
--	public.ad_kraje.platiod,
--	public.ad_kraje.idtransakce,
--	public.ad_kraje.globalniidnavrhuzmeny,
--	public.ad_kraje.nutslau,
--	public.ad_kraje.datumvzniku,
--	public.ad_kraje.definicnibod,
--	public.ad_kraje_orighranice1.geom originalnihranice
-- FROM public.ad_kraje
-- LEFT OUTER JOIN public.ad_kraje_orighranice1 ON (public.ad_kraje.kod=public.ad_kraje_orighranice1.kod);

CREATE TABLE ad_kraje2 AS
SELECT
	public.ad_kraje1.ogc_fid,
	public.ad_kraje1.gml_id,
	public.ad_kraje1.kod,
	public.ad_kraje1.nazev,
	public.ad_kraje1.nespravny,
	public.ad_kraje1.statkod,
	public.ad_kraje1.platiod,
	public.ad_kraje1.idtransakce,
	public.ad_kraje1.globalniidnavrhuzmeny,
	public.ad_kraje1.nutslau,
	public.ad_kraje1.datumvzniku,
	public.ad_kraje1.definicnibod,
	public.ad_kraje1.originalnihranice,
	public.ad_kraje_generhranice1.geom generalizovanehranice
FROM public.ad_kraje1
LEFT OUTER JOIN public.ad_kraje_generhranice1 ON (public.ad_kraje1.kod=public.ad_kraje_generhranice1.kod);

-- Index: ad_kraje_definicnibod_geom_idx

-- DROP INDEX public.ad_kraje_definicnibod_geom_idx;

CREATE INDEX ad_kraje_definicnibod_geom_idx
    ON public.ad_kraje USING gist
    (definicnibod)
    TABLESPACE pg_default;

-- Index: ad_kraje_generalizovanehranice_geom_idx

-- DROP INDEX public.ad_kraje_generalizovanehranice_geom_idx;

CREATE INDEX ad_kraje_generalizovanehranice_geom_idx
    ON public.ad_kraje USING gist
    (generalizovanehranice)
    TABLESPACE pg_default;

-- Index: ad_kraje_originalnihranice_geom_idx

-- DROP INDEX public.ad_kraje_originalnihranice_geom_idx;

CREATE INDEX ad_kraje_originalnihranice_geom_idx
    ON public.ad_kraje USING gist
    (originalnihranice)
    TABLESPACE pg_default;

-- Index: ad_kraje_kod_idx

-- DROP INDEX public.ad_kraje_kod_idx;

CREATE INDEX ad_kraje_kod_idx
    ON public.ad_kraje USING btree
    (kod ASC NULLS LAST)
    TABLESPACE pg_default;
