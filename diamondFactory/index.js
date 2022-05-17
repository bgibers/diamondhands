const trianglify = require('trianglify')
var colors = require('nice-color-palettes');
const fs = require('fs')

for(var i = 0; i < 1000; i ++) {

    var colorFunction = getRandom(1,1000) % 2 ? trianglify.colorFunctions.shadows(getRandom(.2,1)) : trianglify.colorFunctions.sparkle(getRandom(.2,1));
    
    const defaultOptions = {
        width: 1500,
        height: 1500,
        cellSize: getRandom(25,50),//25-50
        variance: 1, // random bw 0-1
        seed: null,
        xColors: 'random',
        yColors: 'random',
        fill: true,
        colorSpace: 'lab',
        palette: colors,
        colorFunction: colorFunction, // sparkle and shadow .2 - 1 random
        strokeWidth: 0
    }
    
    const canvas = trianglify(defaultOptions).toCanvas()
    const file = fs.createWriteStream(`../ipfs/assets/backgrounds/trianglify${i}.png`)
    canvas.createPNGStream().pipe(file)
}

function getRandom(min, max) {
    return Math.random() * (max - min) + min;
  }
