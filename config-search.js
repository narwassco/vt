require('dotenv').config();

module.exports = {
    db: {
      user:process.env.db_'postgres',
      password:process.env.db_'N@rw@ssc0',
      host:process.env.db_'localhost',
      port:process.env.db_'5432',
      database:'narwassco',
    },
    layers : [
        {
          name: 'meter',
          geojsonFileName: __dirname + '/public/meter.geojson',
          select:`
          SELECT row_to_json(featurecollection) AS json FROM (
            SELECT
              'FeatureCollection' AS type,
              array_to_json(array_agg(feature)) AS features
            FROM (
              SELECT
              'Feature' AS type,
              ST_AsGeoJSON(ST_TRANSFORM(x.geom,4326))::json AS geometry,
              row_to_json((
                SELECT p FROM (
                  SELECT
                  x.meterid as fid,
                  CASE WHEN x.connno=-1 THEN NULL ELSE LPAD(CAST(x.connno as text), 4, '0') || x.zonecd END as connno,
                  b.serialno,
                  b.name as customer,
                  c.name as village
                ) AS p
              )) AS properties
              FROM meter x
              INNER JOIN metertype a
              ON x.metertypeid = a.metertypeid
              LEFT JOIN customer b
              ON x.zonecd = b.zonecd
              AND x.connno = b.connno
              LEFT JOIN village c
			        on b.villageid = c.villageid
              WHERE NOT ST_IsEmpty(x.geom) AND x.metertypeid = 1
            ) AS feature
          ) AS featurecollection
          `
        },
    ],
};
