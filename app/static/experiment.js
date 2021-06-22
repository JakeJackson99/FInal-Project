var scroller = document.querySelector("#scroller");
var template = document.querySelector("#post_template");
var sentinel = document.querySelector("#sentinel");

var counter = 0;
var totalSeconds = 0;
var page_type = Math.floor(Math.random() * 2) + 1;

setInterval(setTime, 1000);

/**
 * Makes a request to /load, receives an object, and then implements its contents into the HTML.
 * It makes a clone of the template #post_template for each entry in the received object.
 */
function loadItems() {
  fetch(`/load?c=${counter}&page_type=${page_type}`).then((response) =>
    response.json().then((data) => {
      if (!data.length) {
        sentinel.innerHTML = "No more posts";
        return;
      }

      for (var i = 0; i < data.length; i++) {
        let template_clone = template.content.cloneNode(true);
        template_clone.querySelector("#title").innerHTML = data[i][0];
        template_clone.querySelector("#content").innerHTML = data[i][1];
        scroller.appendChild(template_clone);
        counter += 1;
      }
    })
  );
}

/**
 * Turns the user's behaviours in an object and sends it to /.../submit.
 */
function sendData() {
  var data = {
    page_type: page_type,
    time: totalSeconds,
  };

  fetch("/experiment/submit", {
    method: "POST",
    body: JSON.stringify(data),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
    }),
  });
}

/**
 * Increments 'totalSeconds' every second via 'setInterval()'.
 */
function setTime() {
  ++totalSeconds;
}

/**
 * Creates an IntersectionObserver object to check whether 'entries' is in view. If so, it triggers loadItems().
 * Else, it simple returns.
 */
var intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  loadItems();
});

intersectionObserver.observe(sentinel);
