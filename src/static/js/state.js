// JavaScript Document
document.getElementById("state_submit").addEventListener("click", submit_state);
document.getElementById("state_reset").addEventListener("click", reset_state);
function submit_state() {
  var txt = document.getElementById('state_txt').value; //獲取textarea的值
  alert(txt);
}
function reset_state() {
 	$("#state_txt").val('');//清空textarea的值
}


document.getElementById("note_submit").addEventListener("click", submit_note);
document.getElementById("note_reset").addEventListener("click", reset_note);

function submit_note() {
  var txt = document.getElementById('note_txt').value; //獲取textarea的值
  alert(txt);
}
function reset_note() {
 	$("#note_txt").val('');//清空textarea的值
}