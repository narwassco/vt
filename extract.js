const {Mbtiles2Pbf, FileExtension} = require('@watergis/mbtiles2pbf');
const fs = require('fs');

const config = require('./config-extract');

const extract = async() =>{
    console.time('mbtiles2pbf');
    if (!fs.existsSync(config.mbtiles)){
        console.log(`${config.mbtiles} does not exists. Skipped!`);
        return;
    }
    const mb2pbf = new Mbtiles2Pbf(config.mbtiles, config.ghpages.tiles, FileExtension.MVT);
    const no_tiles = await mb2pbf.run();
    console.log(`${no_tiles} tiles were extracted under ${config.ghpages.tiles}`);
    console.timeEnd('mbtiles2pbf');
};

module.exports = extract();