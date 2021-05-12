-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
DROP TABLE IF EXISTS gids;
CREATE TABLE gids AS SELECT gid FROM address_points GROUP BY gid ORDER BY gid;

-- Index: gids_gid_idx

-- DROP INDEX public.gids_gid_idx;

CREATE INDEX gids_gid_idx
    ON public.gids USING btree
    (gid ASC NULLS LAST)
    TABLESPACE pg_default;
