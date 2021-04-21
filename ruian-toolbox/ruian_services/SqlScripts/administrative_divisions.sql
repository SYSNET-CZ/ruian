-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################

DROP TABLE IF EXISTS public.administrative_division;
CREATE TABLE public.administrative_division
AS SELECT
	public.parcely.id gid,
	public.parcely.kmenovecislo cislo_parc,
	public.parcely.pododdelenicisla cislo_parc_2,
	public.parcely.vymeraparcely vymera,
	public.parcely.katastralniuzemikod kod_ku,
	public.katastralniuzemi.nazev nazev_ku,
	public.katastralniuzemi.obeckod kod_obec,
	public.obce.nazev nazev_obec,
	public.obce.statuskod kod_obec_status,
	public.obce.okreskod kod_okres,
	public.obce.poukod kod_pou,
	public.okresy.nazev nazev_okres,
	public.okresy.krajkod kod_kraj,
	public.okresy.vusckod kod_vusc,
	public.pou.nazev nazev_pou,
	public.pou.orpkod kod_orp,
	public.kraje.nazev nazev_kraj,
	public.kraje.statkod kod_stat,
	public.vusc.nazev nazev_vusc,
	public.vusc.regionsoudrznostikod kod_nuts2,
	public.vusc.nutslau nuts_3,
	public.orp.nazev nazev_orp,
	public.staty.nazev nazev_stat,
	public.staty.nutslau nuts_1,
	public.regionysoudrznosti.nazev nazev_nuts2,
	public.regionysoudrznosti.nutslau nuts_2,
	public.parcely.platiod plati_od,
	public.parcely.originalnihranice geom
FROM 
	public.parcely
	LEFT OUTER JOIN public.katastralniuzemi ON (public.parcely.katastralniuzemikod=public.katastralniuzemi.kod)
	LEFT OUTER JOIN public.obce ON (public.katastralniuzemi.obeckod=public.obce.kod)
	LEFT OUTER JOIN public.okresy ON (public.obce.okreskod=public.okresy.kod)
	LEFT OUTER JOIN public.pou ON (public.obce.poukod=public.pou.kod)
	LEFT OUTER JOIN public.kraje ON (public.okresy.krajkod=public.kraje.kod)
	LEFT OUTER JOIN public.vusc ON (public.okresy.vusckod=public.vusc.kod)
	LEFT OUTER JOIN public.orp ON (public.pou.orpkod=public.orp.kod)
	LEFT OUTER JOIN public.staty ON (public.kraje.statkod=public.staty.kod)
	LEFT OUTER JOIN public.regionysoudrznosti ON (public.vusc.regionsoudrznostikod=public.regionysoudrznosti.kod);

ALTER TABLE public.administrative_division ADD PRIMARY KEY (gid);

SELECT UpdateGeometrySRID('public', 'administrative_division', 'geom', 5514);

CREATE INDEX administrative_division_geom_idx
  ON public.administrative_division
  USING GIST (geom);

