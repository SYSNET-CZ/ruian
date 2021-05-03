-- ##################################################
-- Tento SQL skript se spustí po importu dat do databáze
-- Eliminuje duplikované řádky ve všech tabulkách RUIAN. Ponechá nejnovější hodnoty.
-- ##################################################
DELETE FROM adresnimista a USING adresnimista b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM castiobci a USING castiobci b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM katastralniuzemi a USING katastralniuzemi b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM momc a USING momc b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM mop a USING mop b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM obce a USING obce b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM okresy a USING okresy b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM orp a USING orp b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM parcely a USING parcely b WHERE a.ogc_fid < b.ogc_fid AND a.id = b.id;
DELETE FROM pou a USING pou b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM regionysoudrznosti a USING regionysoudrznosti b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM spravniobvody a USING spravniobvody b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM staty a USING staty b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM stavebniobjekty a USING stavebniobjekty b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM ulice a USING ulice b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM vusc a USING vusc b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;
DELETE FROM zsj a USING zsj b WHERE a.ogc_fid < b.ogc_fid AND a.kod = b.kod;