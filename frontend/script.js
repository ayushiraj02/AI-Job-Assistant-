const API_BASE_URL = "http://127.0.0.1:8000/api";

const resumeTextEl = document.getElementById("resumeText");
const statusEl = document.getElementById("status");
const findJobsBtn = document.getElementById("findJobsBtn");
const jobListEl = document.getElementById("jobList");

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#b42318" : "#4f6354";
}

async function uploadResumeText() {
  const text = resumeTextEl.value.trim();
  if (!text) {
    throw new Error("Please paste resume text first.");
  }

  const response = await fetch(`${API_BASE_URL}/resume`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || "Failed to upload resume text.");
  }
}

async function fetchJobs() {
  const response = await fetch(`${API_BASE_URL}/jobs`);
  if (!response.ok) {
    throw new Error("Failed to fetch jobs.");
  }
  return response.json();
}

async function fetchMatchScore(jobId) {
  const response = await fetch(`${API_BASE_URL}/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_id: jobId }),
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || "Failed to calculate match score.");
  }

  const data = await response.json();
  return data.match_percentage;
}

function createJobCard(job, score) {
  const card = document.createElement("article");
  card.className = "job-card";

  card.innerHTML = `
    <div class="job-head">
      <div>
        <h3 class="job-title">${job.title}</h3>
        <p class="company">${job.company}</p>
      </div>
      <span class="match-pill">${score}% Match</span>
    </div>
    <p class="job-desc">${job.description}</p>
    <button class="btn-secondary" type="button">Auto Apply</button>
  `;

  const autoApplyBtn = card.querySelector("button");
  autoApplyBtn.addEventListener("click", () => {
    setStatus(`Auto applied to ${job.title} at ${job.company}.`);
  });

  return card;
}

async function findJobsWithScores() {
  findJobsBtn.disabled = true;
  findJobsBtn.textContent = "Finding...";
  setStatus("Uploading resume and fetching jobs...");
  jobListEl.innerHTML = "";

  try {
    await uploadResumeText();
    const jobs = await fetchJobs();

    if (!Array.isArray(jobs) || jobs.length === 0) {
      setStatus("No jobs found right now.");
      return;
    }

    setStatus("Calculating match scores...");

    const scoreTasks = jobs.map(async (job) => {
      const score = await fetchMatchScore(job.id);
      return { job, score };
    });

    const scoredJobs = await Promise.all(scoreTasks);
    scoredJobs.sort((a, b) => b.score - a.score);

    scoredJobs.forEach(({ job, score }) => {
      jobListEl.appendChild(createJobCard(job, score));
    });

    setStatus(`Found ${scoredJobs.length} jobs with match scores.`);
  } catch (error) {
    setStatus(error.message || "Something went wrong.", true);
  } finally {
    findJobsBtn.disabled = false;
    findJobsBtn.textContent = "Find Jobs";
  }
}

findJobsBtn.addEventListener("click", findJobsWithScores);
