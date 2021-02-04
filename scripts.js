var c = document.getElementById("sCanvas");
var ctx = c.getContext("2d");
ctx.fillStyle = "#c0ecff";
ctx.fillRect(0, 0, 1200, 500);


ctx.beginPath();

ctx.fillStyle = "#FFFFFF";
for (i = 0; i < 24; i++) {
    var amount = parseInt(document.getElementById("hour" + i.toString(10)).innerHTML);

    ctx.moveTo(i * 50, 500 - amount / 2);
    ctx.lineTo(i * 50 + 50, 500 - amount / 2);
    ctx.fillRect(i * 50, 500 - amount / 2, 50, amount / 2);
}
ctx.stroke();


ctx.beginPath();
var i = 0;
for (i = 0; i < 25; i++) {
    ctx.moveTo(i * 50, 0);
    ctx.lineTo(i * 50, 500);
} 
ctx.moveTo(0, 0);
ctx.lineTo(1200, 0);
ctx.moveTo(0, 500);
ctx.lineTo(1200, 500);
ctx.stroke();

document.getElementById("paivanKeskiarvo").innerHTML = paivanKeski();

function paivanKeski() {
    var keskiArvo = 0;
    for (i = 0; i < 24; i++) {
        var amount = parseInt(document.getElementById("hour" + i.toString(10)).innerHTML);
        keskiArvo += amount;
    }
    keskiArvo /= 24;
    return keskiArvo;
}