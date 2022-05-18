const trianglify = require('trianglify')
var colors = require('nice-color-palettes');
const fs = require('fs')

for(var i = 0; i < 1000; i ++) {

    var colorFunction;
    var metadata = {
      "Chroma type" : "shadow",
      "Diamond size" : "25",
      "Diamond variance" : "1",
      "Color1" : "2",
      "Color2" : "2",
      "Color3" : "2",
      "Color4" : "2",
      "Color5" : "2"
    }

    if (randomInteger(1,2) % 2) {
      colorFunction = trianglify.colorFunctions.shadows(getRandom(.2,1));
      metadata['Chroma type'] = "shadow";
    } else {
      colorFunction = trianglify.colorFunctions.sparkle(getRandom(.2,1));
      metadata['Chroma type'] = "sparkle";
    }

    var cellSize = getRandom(25,50);
    metadata['Diamond size'] = cellSize;

    var cellVar = getRandom(.6, 1);
    metadata['Diamond variance'] = cellVar;

    var color = [colors[randomInteger(0,99)]]
    metadata.Color1 = color[0][0],
    metadata.Color2 = color[0][1],
    metadata.Color3 = color[0][2],
    metadata.Color4 = color[0][3],
    metadata.Color5 = color[0][4]

    const defaultOptions = {
        width: 1500,
        height: 1500,
        cellSize: cellSize,//25-50
        variance: cellVar, // random bw 0-1
        seed: null,
        xColors: 'random',
        yColors: 'random',
        fill: true,
        colorSpace: 'lab',
        palette: color,
        colorFunction: colorFunction, // sparkle and shadow .2 - 1 random
        strokeWidth: 0
    }
    
    const canvas = trianglify(defaultOptions).toCanvas()
    const file = fs.createWriteStream(`../ipfs/assets/backgrounds/trianglify${i}.png`)
    canvas.createPNGStream().pipe(file)

    fs.writeFile(`../ipfs/assets/metadata/trianglify${i}.json`, JSON.stringify(metadata), () => {})
}

function getRandom(min, max) {
    return Math.random() * (max - min) + min;
}

function randomInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
