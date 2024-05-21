const scrollers = document.querySelectorAll(".scroller");

if (!window.matchMedia("(prefers-reduced-motion: redice)").matches) {
    addAnimation();
}

function addAnimation() {
    scrollers.forEach(scroller => {
        scroller.setAttribute("data-animated", true);

        const scrollerInner = scroller.querySelector(".sc-inner");
        const scrollerContent = Array.from(scrollerInner.children);

        scrollerContent.forEach(item => {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute('aria-hidden', true);
            scrollerInner.appendChild(duplicatedItem);
        })
    })
}

document.addEventListener("DOMContentLoaded", (event) => {
    var notification = document.getElementById('notification');

    if (notification.textContent != "") {
        console.log(notification)
        document.getElementById("js-alert-box").classList.add('notif-box-op');
        setTimeout(function () {
            document.getElementById("js-alert-box").classList.remove('notif-box-op');
            document.getElementById("js-alert-box").classList.add('notif-box-close');
        }, 4000);
    }
  }
);

