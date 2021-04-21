-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
DROP TABLE IF EXISTS gids;
CREATE TABLE gids AS SELECT gid FROM address_points GROUP BY gid ORDER BY gid;
