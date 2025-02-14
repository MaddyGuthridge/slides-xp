/**
 * Navigator.js
 *
 * Navigate between slides
 */


window.addEventListener("keydown", e => {
  switch (e.key) {
    case "ArrowLeft":
      if (window.sxp.prev) {
        window.location.pathname = window.sxp.prev;
      }
      break;
    case "ArrowRight":
      if (window.sxp.next) {
        window.location.pathname = window.sxp.next;
      }
      break;
      break;
  }
});
