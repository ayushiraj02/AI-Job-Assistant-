const API_BASE_URL = "http://127.0.0.1:8000/api";

const resumeTextEl = document.getElementById("resumeText");
const statusEl = document.getElementById("status");
const findJobsBtn = document.getElementById("findJobsBtn");
const loadingIndicatorEl = document.getElementById("loadingIndicator");
const jobListEl = document.getElementById("jobList");
const autoApplyToggleEl = document.getElementById("autoApplyToggle");
const toggleStateEl = document.getElementById("toggleState");
const totalJobsEl = document.getElementById("totalJobs");
const appliedCountEl = document.getElementById("appliedCount");
const appliedPercentEl = document.getElementById("appliedPercent");
const appliedJobsListEl = document.getElementById("appliedJobsList");

let scoredJobsState = [];
let appliedJobsState = [];

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? "#b42318" : "#4f6354";
}

function showJobEmptyState(message) {
  jobListEl.innerHTML = `<div class="empty-state">${message}</div>`;
}

function setLoading(isLoading) {
  loadingIndicatorEl.classList.toggle("hidden", !isLoading);
}

function getMatchClass(score) {
  if (score >= 75) {
    return "match-high";
  }
  if (score >= 45) {
    return "match-medium";
  }
  return "match-low";
}

async function uploadResumeText() {
  const text = resumeTextEl.value.trim();
  if (!text) {
    throw new Error("Please enter resume to continue");
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
  return {
    score: data.match_percentage,
    matchedSkills: data.matched_skills || [],
    missingSkills: data.missing_skills || [],
  };
}

async function triggerAutoApply() {
  const response = await fetch(`${API_BASE_URL}/auto-apply`, {
    method: "POST",
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || "Failed to auto apply jobs.");
  }

  const data = await response.json();
  return data.applied_jobs || [];
}

async function fetchAppliedJobs() {
  const response = await fetch(`${API_BASE_URL}/applied-jobs`);
  if (!response.ok) {
    throw new Error("Failed to fetch applied jobs.");
  }

  const data = await response.json();
  return data.applied_jobs || [];
}

function isApplied(jobId) {
  return appliedJobsState.some((job) => job.id === jobId);
}

function renderAppliedJobsDashboard() {
  const totalJobsFound = scoredJobsState.length;
  const appliedCount = scoredJobsState.filter(({ job }) => isApplied(job.id)).length;
  const appliedPercent = totalJobsFound > 0 ? (appliedCount / totalJobsFound) * 100 : 0;

  totalJobsEl.textContent = String(totalJobsFound);
  appliedCountEl.textContent = String(appliedCount);
  appliedPercentEl.textContent = `${appliedPercent.toFixed(1)}%`;
  appliedJobsListEl.innerHTML = "";

  if (appliedJobsState.length === 0) {
    appliedJobsListEl.innerHTML = '<p class="applied-meta">No jobs applied yet.</p>';
    return;
  }

  appliedJobsState
    .slice()
    .sort((a, b) => b.match_percentage - a.match_percentage)
    .forEach((job) => {
      const item = document.createElement("div");
      item.className = "applied-item";
      item.innerHTML = `
        <div>
          <p><strong>${job.title}</strong> · ${job.company}</p>
          <p class="applied-meta">Match: ${job.match_percentage}%</p>
        </div>
        <span class="status-pill status-applied">Applied</span>
      `;
      appliedJobsListEl.appendChild(item);
    });
}

function setToggleStateLabel() {
  if (autoApplyToggleEl.checked) {
    toggleStateEl.textContent = "ON";
    return;
  }
  toggleStateEl.textContent = "OFF";
}

function createJobCard(job, score, matchedSkills, missingSkills) {
  const card = document.createElement("article");
  card.className = "job-card";

  const applied = isApplied(job.id);
  const statusClass = applied ? "status-applied" : "status-not-applied";
  const statusText = applied ? "Applied" : "Not Applied";
  const matchClass = getMatchClass(score);
  const matchedSkillsText = matchedSkills.length > 0 ? matchedSkills.join(", ") : "None";
  const missingSkillsText = missingSkills.length > 0 ? missingSkills.join(", ") : "None";
  const suggestionText =
    missingSkills.length > 0
      ? `You can improve your chances by learning: ${missingSkillsText}`
      : "Great fit: your profile covers the key required skills.";

  card.innerHTML = `
    <div class="job-head">
      <div>
        <h3 class="job-title">${job.title}</h3>
        <p class="company">${job.company}</p>
      </div>
      <div class="match-box">
        <span class="match-pill ${matchClass}">${score}% Match</span>
        <div class="why-match">
          <p class="why-line"><strong>Matched:</strong> ${matchedSkillsText}</p>
          <p class="why-line"><strong>Missing:</strong> ${missingSkillsText}</p>
        </div>
      </div>
    </div>
    <p><span class="status-pill ${statusClass}">${statusText}</span></p>
    <p class="job-desc">${job.description}</p>
    <p class="skill-suggestion">${suggestionText}</p>
    <button class="btn-secondary" type="button">Auto Apply</button>
  `;

  const autoApplyBtn = card.querySelector("button");
  autoApplyBtn.addEventListener("click", async () => {
    try {
      const appliedJobs = await triggerAutoApply();
      appliedJobsState = appliedJobs;
      renderAppliedJobsDashboard();
      renderJobList();
      if (isApplied(job.id)) {
        setStatus(`Applied to ${job.title} at ${job.company}.`);
        return;
      }
      setStatus(`${job.title} did not meet the auto-apply threshold (>70%).`);
    } catch (error) {
      setStatus(error.message || "Auto apply failed.", true);
    }
  });

  return card;
}

function renderJobList() {
  jobListEl.innerHTML = "";
  scoredJobsState.forEach(({ job, score, matchedSkills, missingSkills }) => {
    jobListEl.appendChild(createJobCard(job, score, matchedSkills, missingSkills));
  });
}

async function findJobsWithScores() {
  findJobsBtn.disabled = true;
  findJobsBtn.textContent = "Finding...";
  setLoading(true);
  setStatus("Uploading resume and fetching jobs...");
  jobListEl.innerHTML = "";

  try {
    await uploadResumeText();
    const jobs = await fetchJobs();

    if (!Array.isArray(jobs) || jobs.length === 0) {
      scoredJobsState = [];
      renderAppliedJobsDashboard();
      showJobEmptyState("No matching jobs found");
      setStatus("No matching jobs found");
      return;
    }

    setStatus("Calculating match scores...");

    const scoreTasks = jobs.map(async (job) => {
      const matchData = await fetchMatchScore(job.id);
      return {
        job,
        score: matchData.score,
        matchedSkills: matchData.matchedSkills,
        missingSkills: matchData.missingSkills,
      };
    });

    scoredJobsState = await Promise.all(scoreTasks);
    scoredJobsState.sort((a, b) => b.score - a.score);

    if (autoApplyToggleEl.checked) {
      setStatus("Auto Apply is ON. Applying matched jobs...");
      appliedJobsState = await triggerAutoApply();
    } else {
      appliedJobsState = await fetchAppliedJobs();
    }

    renderAppliedJobsDashboard();
    renderJobList();

    setStatus(`Found ${scoredJobsState.length} jobs. Applied: ${appliedJobsState.length}.`);
  } catch (error) {
    if (error.message === "Please enter resume to continue") {
      showJobEmptyState("Please enter resume to continue");
    }
    setStatus(error.message || "Something went wrong.", true);
  } finally {
    findJobsBtn.disabled = false;
    findJobsBtn.textContent = "Find Jobs";
    setLoading(false);
  }
}

autoApplyToggleEl.addEventListener("change", setToggleStateLabel);
findJobsBtn.addEventListener("click", findJobsWithScores);

setToggleStateLabel();
renderAppliedJobsDashboard();
setLoading(false);
