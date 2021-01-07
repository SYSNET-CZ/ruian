-- ##################################################
-- This script creates reverse geolocation table
-- ##################################################


DROP TABLE IF EXISTS administrative_division;
CREATE TABLE administrative_division
AS SELECT
	parcely.id gid, 
	parcely.kmenovecislo cislo_parc, 
	parcely.pododdelenicisla cislo_parc_2, 
	parcely.vymeraparcely vymera,
	parcely.katastralniuzemikod kod_ku,
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
	parcely.platiod plati_od,
	parcely.originalnihranice geom
FROM 
	parcely
	LEFT OUTER JOIN katastralniuzemi ON (parcely.katastralniuzemikod=katastralniuzemi.kod)
	LEFT OUTER JOIN obce ON (katastralniuzemi.obeckod=obce.kod)
	LEFT OUTER JOIN okresy ON (obce.okreskod=okresy.kod)
	LEFT OUTER JOIN pou ON (obce.poukod=pou.kod)
	LEFT OUTER JOIN kraje ON (okresy.krajkod=kraje.kod)
	LEFT OUTER JOIN vusc ON (okresy.vusckod=vusc.kod)
	LEFT OUTER JOIN orp ON (pou.orpkod=orp.kod)
	LEFT OUTER JOIN staty ON (kraje.statkod=staty.kod)
	LEFT OUTER JOIN regionysoudrznosti ON (vusc.regionsoudrznostikod=regionysoudrznosti.kod);

ALTER TABLE administrative_division ADD PRIMARY KEY (gid);

SELECT UpdateGeometrySRID('public', 'administrative_division', 'geom', 5514);

CREATE INDEX administrative_division_geom_idx
  ON administrative_division
  USING GIST (geom);

