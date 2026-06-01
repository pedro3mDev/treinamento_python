document.querySelectorAll("input").forEach(input => {
  input.addEventListener("input", (event) => {
    switch (input.type) {
      case "text":
        {
          if (event.target.id === "pesquisa2") {
            if (!isNaN(event.target.value.charAt(0))) {
              event.target.value = event.target.value.replace(/[^0-9]/g, '');
              if (event.target.value.length > 9) {
                event.target.value = event.target.value.substring(0, 9);
            }}else {
              event.target.value = event.target.value.replace(/^\s+|\s{2,}|\s$/g, ' ').replace(/^\s+|\s{3,}|[^a-zA-Z\s]/g, '')
            }
          }
          else  event.target.value = event.target.value.replace(/^\s+|\s{2,}|\s$/g, ' ').replace(/^\s+|\s{3,}|[^a-zA-Z\s]/g, '');
        }
        break;
      case "number":
        {
          event.target.value = event.target.value.replace(/[^0-9]/g, '');
          if (event.target.value.length > 6 && event.target.min == 500) {
            event.target.value = event.target.value.substring(0, 6);
          }
          else if (event.target.value.length > 9 && event.target.min == 100000000) {
            event.target.value = event.target.value.substring(0, 9);
          }
          else if (event.target.value.length > 2 && event.target.max == 99) {
            event.target.value = event.target.value.substring(0, 9);
          }
          else if (event.target.value > 350 && event.target.max == 350) {
            event.target.value = event.target.value.substring(0, 3);
            event.target.value = 350;

          }
        }
        break;
    }
  });
});
document.querySelectorAll("input").forEach(input => {
  input.addEventListener("blur", (event) => {
    event.target.value = event.target.value.trim();
  });
});