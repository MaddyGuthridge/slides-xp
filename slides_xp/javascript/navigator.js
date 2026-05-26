/**
 * Navigator.js
 *
 * Listen for keyboard shortcuts to allow for slide navigation.
 */


 function toggleFullScreen() {
  if (document.fullscreenElement == null) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}

window.addEventListener("keydown", e => {
  const root = `${window.location.protocol}//${window.location.host}/`;

  let target = null;
  switch (e.key) {
    case "0":
      if (window.sxp.prev) {
        target = `${root}${window.sxp.first}`;
      }
      break;
    case "f":
      toggleFullScreen();
      break;
    case "ArrowLeft":
      if (window.sxp.prev) {
        target = `${root}${window.sxp.prev}`;
      }
      break;
    case "ArrowRight":
      if (window.sxp.next) {
        target = `${root}${window.sxp.next}`;
      }
      break;
    case "Escape":
      target = root;
      break;
  }
  if (target !== null) {
    // change body to next page
    htmx.ajax('GET', target, { target: 'body', swap: 'innerHTML', push: true });
    e.preventDefault();
  }
});

// When state is popped from history
window.onpopstate = () => {
  // Get previous page and swap it in
  htmx.ajax('GET', window.location.pathname, {
    target: 'body',
    swap: 'innerHTML'
    // Do NOT include push: true here, or it will loop history entries
  });
};
