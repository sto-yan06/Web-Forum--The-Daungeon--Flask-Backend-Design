const audio = document.getElementById("background-audio");
const volumeRange = document.getElementById("volume-range");
const audioButton = document.getElementById("audio-control-button")

audio.volume = 0.1;

function handleVolumeControl(){
    const volumeValue = parseFloat(volumeRange.value);
    audio.volume = volumeValue;
}

function handleAudioControl(){
    if(audio.paused){
        audio.play();
        audioButton.textContent = "Pause Audio";
    }
    else{
        audio.pause();
        audioButton.textContent = "Start Audio";
    }
}


volumeRange.addEventListener("input", handleVolumeControl);
audioButton.addEventListener("click", handleAudioControl);

const mediaQuery = window.matchMedia("(max-width: 768px)");

function checkMediaQuery(){
    if(mediaQuery.matches){
        volumeRange.removeEventListener("input", handleVolumeControl);
        audioButton.removeEventListener("click", handleAudioControl);

        volumeRange.addEventListener("input", ()=> {
            if(audio.paused){
                audio.play();
                audioButton.textContent = "Pause Audio";
            }
            else{
                audio.pause();
                audioButton.textContent ="Start Audio";
            }
        });
    }
}

checkMediaQuery();
mediaQuery.addListener(checkMediaQuery);

//Light cursor
var pos = document.documentElement;
pos.addEventListener('mousemove', e =>{
    pos.style.setProperty('--x', e.clientX + 'px')
    pos.style.setProperty('--y', e.clientY + 'px')
})

document.getElementById("join-button").onclick = function(){
    location.href = "/registration";
};