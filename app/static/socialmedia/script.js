function change() {
  const content = document.getElementById("username").value;
  document.getElementById("count").innerHTML = content.length;
  console.log(content.length);
}
