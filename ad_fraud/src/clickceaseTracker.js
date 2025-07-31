let totalBehaviour = [];
let mousemoveTimes = [];
let mousemoveTotalBehaviour = [];
const sessionId = crypto.randomUUID();

let startTime;

// New: Track unique URLs hovered over by mouse
const hoveredUrls = new Set();

function startTracking() {
  console.log("Tracking started for session:", sessionId);
  startTime = Date.now();

  document.addEventListener("mousemove", handleMousemove);
  document.addEventListener("click", handleClick);
  document.addEventListener("contextmenu", handleRightClick);
  document.addEventListener("auxclick", handleMiddleClick);

  // New: Track links hovered over by mouse
  document.querySelectorAll("a").forEach(link => {
    link.addEventListener("mouseover", () => {
      const href = link.getAttribute("href");
      if (href) hoveredUrls.add(href);
    });
  });
}

function endTracking() {
  console.log("Ending tracking for session:", sessionId);

  const payload = {
    session_id: sessionId,
    total_behaviour: totalBehaviour,
    mousemove_times: mousemoveTimes,
    mousemove_total_behaviour: mousemoveTotalBehaviour,
    Mousemove_visited_urls: hoveredUrls.size // New field added
  };

  fetch("http://localhost:5000/log-visit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload),
    keepalive: true
  }).then(res => {
    if (!res.ok) {
      console.error("Failed to send tracking data:", res.statusText);
    } else {
      console.log("Sent tracking data");
    }
  }).catch(err => {
    console.error("Error sending tracking data:", err);
  });
}

function handleMousemove(e) {
  const now = Date.now();
  totalBehaviour.push(`m(${e.clientX},${e.clientY})`);
  mousemoveTotalBehaviour.push({ x: e.clientX, y: e.clientY });
  mousemoveTimes.push(now - startTime);
}

function handleClick() {
  mousemoveTimes.push(Date.now() - startTime);
  totalBehaviour.push("c(l)");
}
function handleRightClick() {
  mousemoveTimes.push(Date.now() - startTime);
  totalBehaviour.push("c(r)");
}
function handleMiddleClick() {
  mousemoveTimes.push(Date.now() - startTime);
  totalBehaviour.push("c(m)");
}

export { startTracking, endTracking };
if (typeof window !== "undefined") {
  window.endTracking = endTracking;
  window.startTracking = startTracking;
}