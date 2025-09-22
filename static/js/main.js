let countdown = 60;
const timerEl = document.getElementById("timer");
const refreshBtn = document.getElementById("refreshBtn");

function fetchJobs() {
    fetch("/api/jobs")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#jobsTable tbody");
            tbody.innerHTML = "";
            data.forEach(job => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${job.title}</td>
                    <td>${job.ref_no}</td>
                    <td>${job.location}</td>
                    <td>${job.type}</td>
                    <td>${job.published_date}</td>
                    <td>${job.is_new ? "Yes" : ""}</td>
                    <td><a href="${job.link}" target="_blank">Link</a></td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function updateCountdown() {
    countdown--;
    if(countdown <= 0){
        fetchJobs();
        countdown = 60;
    }
    timerEl.textContent = countdown;
}

refreshBtn.addEventListener("click", () => {
    fetch("/api/check-now")
        .then(res => res.json())
        .then(() => {
            fetchJobs();
            countdown = 60;
        });
});

fetchJobs();
setInterval(updateCountdown, 1000);