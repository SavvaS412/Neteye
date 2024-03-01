function fetchNotifications() {
    fetch("/api/notifications", {
        method: "GET"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle the JSON data here
        console.log(data); // For demonstration, you can replace this with your desired processing logic
        const counter = document.getElementById("bell-counter");

        if (data.length > 0) {
            if (data.length > 9)
                counter.innerText = "+9";
            else
                counter.innerText = data.length;
            counter.hidden = false;
            for (const notification of data) {
                showNotification(notification);
            }
        }
        else {
            counter.hidden = true;
        }
    })
    .catch(error => {
        console.error("Couldn't fetch from '/api/notifications':", error);
    });
}

window.onload = function () {
    fetchNotifications();
    const updateInterval = 15000      //TODO: change this to take out of settings
    setInterval(fetchNotifications, updateInterval);
}

const template = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="toast-image" viewBox="0 0 16 16">
<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
<path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
</svg>`

function showNotification(notification) {
    const toastBox = document.getElementById('toast-box');
    let anchor = document.createElement('a');
    anchor.href = "/notifications/" + notification.id;
    anchor.classList.add('toast');
    let toast = document.createElement('div');
    toast.classList.add('toast', 'fade-in');
    toast.innerHTML = getNotificationHTML(notification);
    anchor.appendChild(toast);
    toastBox.appendChild(anchor);

    setTimeout(() => {
        toast.classList.remove('fade-in'); // Remove 'fade-in' class
        toast.classList.add('fade-out'); // Add 'fade-out' class
        setTimeout(() => {
            anchor.remove(); // Remove the notification from DOM after fade out
        }, 3000); // Wait for 3 seconds for fade out animation to complete
    }, 10000); // TODO: Wait for 6 seconds before starting fade-out animation (2 seconds fade-in + 8 seconds visible)  - change this to take out of settings

}

function getNotificationHTML(notification) {
    return template + `
    <h3 class="notification-toast-name">${notification.name}</h3>
    <p class="notification-toast-type">${notification.type}</p>
    <p class="notification-toast-date">${notification.date}</p>`;
}