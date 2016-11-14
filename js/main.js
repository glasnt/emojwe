// vars, settings, & selectors
/////////////////////////////
var canvas = document.querySelector('.canvas');
var ctx = canvas.getContext('2d');

var imgs, loaded, count, percent, finished, timeout;
var outIdx = 0, inIdx = 1;
var imgOrder = ['0', '3', '6', '4', '1-2', '5'];

var currEmoji = 'sign-of-the-horns';
var currPlatform = 'apple';

var gif, gifBlob, gifConfig = {
  repeat: 0,
  quality: 1,
  workers: 2,
  workerScript: 'js/vendor/gif.worker.js'
};

var fadeMs = 40
var pauseMs = 300;

var form = document.querySelector('.emoji-options');
var gifBtn = document.querySelector('.make-gif');
var gifDone = document.querySelector('.gif-done');

// event handlers
/////////////////////////////
gifBtn.addEventListener('click', gifify);
form.addEventListener('change', update);

// main & helper methods
/////////////////////////////
function run(emoji, platform) {
  reset();
  var urls = getImgUrls(emoji, platform);
  for (var i = 0; i < urls.length; i++) {
    var img = new Image();
    imgs.push(img);
    img.onload = function () {
      loaded++;
      if (loaded === urls.length) {
        canvas.width = canvas.height = (platform == 'apple' ? 160 : 240);
        ctx.drawImage(imgs[0], 0, 0);
        setTimeout(animate, 200);
      }
    };
    img.src = urls[i];
  }
}

function reset() {
  imgs = [];
  loaded = 0;
  count = 0;
  percent = 0;
  finished = false;
  outIdx = 0;
  inIdx = 1;
  clearTimeout(timeout);
  gif = new GIF(gifConfig);
  gifBlob = null;
}

function getImgUrls(e, p) {
  return imgOrder.map(function(t) { return 'img/' + e + '/' + p + '/' + t + '.jpg'; });
}

function animate() {
  draw(imgs[inIdx], percent / 100);
  draw(imgs[outIdx], (1 - percent / 100));

  if (percent >= 100) { next(); return; }

  // add current canvas state as gif frame
  if (!finished && percent % 5 === 0) {
    gif.addFrame(canvas, { delay: fadeMs, copy: true });
  }

  percent += 5;
  timeout = setTimeout(animate, fadeMs);
}

function next() {
  if (!finished) gif.addFrame(canvas, { delay: pauseMs, copy: true });
  if (++count == imgs.length) { finished = true; }

  inIdx = ++inIdx % imgs.length;
  outIdx = ++outIdx % imgs.length;
  percent = 0;

  setTimeout(animate, pauseMs);
}

function draw(img, opacity) {
  ctx.save();
  ctx.globalAlpha = opacity;
  ctx.drawImage(img, 0, 0);
  ctx.restore();
}

function update() {
  currEmoji = form.querySelector('.select-emoji').value;
  currPlatform = form.querySelector('.select-platform').value;
  run(currEmoji, currPlatform);
}

function gifify() {
  gifBtn.disabled = true;
  gifBtn.innerHTML = 'Creating GIF...';
  build();

  function build() {
    if (!finished) { setTimeout(build, 1000); return; }
    if (gifBlob) { save(); return; }

    gif.running = false;
    gif.render();

    gif.on('progress', function(p) {
      gifBtn.innerHTML = 'Saving GIF... (' + Math.round(p * 100) + '%)';
    });

    gif.on('finished', function(blob) {
      gifBlob = blob;
      save();
    });
  }

  function save() {
    gifBtn.disabled = false;
    gifBtn.innerHTML = 'Download GIF';
    gifDone.setAttribute('data-url', URL.createObjectURL(gifBlob));
    saveAs(gifBlob, currPlatform + '_' + currEmoji + '.gif');
  }
}

// kick things off
/////////////////////////////
run(currEmoji, currPlatform);
