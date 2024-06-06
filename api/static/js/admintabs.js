var li_elements = document.querySelectorAll(".container .navigation li");
var item_elements = document.querySelectorAll(".admintabs");
for (var i = 0; i < li_elements.length; i++) {
  li_elements[i].addEventListener("click", function() {
    li_elements.forEach(function(li) {
      li.classList.remove("activedashboardtab");
    });
    this.classList.add("activedashboardtab");
    var li_value = this.getAttribute("data-li");
    item_elements.forEach(function(item) {
      item.style.display = "none";
    });
    if (li_value == "emptable") {
      document.querySelector("." + li_value).style.display = "block";
    } else if (li_value == "allblogs") {
      document.querySelector("." + li_value).style.display = "block";
    } else if (li_value == "addemp") {
      document.querySelector("." + li_value).style.display = "block";
    } else {
      console.log("");
    }
  });
}
