function change(){
    var button=document.querySelector(".btn2")
    var randomX=Math.floor(Math.random()* 500)
    var randomY=Math.floor(Math.random()* 500)
    button.style.left=randomX+"px";
    button.style.bottom=randomY+"px";
  }
function changeImage() {
            var mainImage = document.getElementById("mainImage");
            mainImage.src ="WG8T.gif" // Replace with the path to your new image
            hideButtons();
        }
function changeText() {
            var textElement = document.getElementById("textElement");
            textElement.innerHTML = "Great! I knew it😍😍.";
        }
function hideButtons() {
            var btn1 = document.querySelector('.btn1');
        var btn2 = document.querySelector('.btn2');
        btn1.classList.add('hidden');
        btn2.classList.add('hidden');
        }
        for (let i=0;i<5;i++) {
            for (let j=0;j<4;j++) {
                console.log("video");
            }
        }
