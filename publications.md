---
layout: default
title: Publications
---

## Metrics

<div class="metrics-dashboard">
    <div class="metric">
        <h3>Total Citations</h3>
        <p id="totalCitations">Loading…</p>
    </div>

    <div class="metric">
        <h3>h-index</h3>
        <p id="hIndex">Loading…</p>
    </div>

    <div class="metric">
        <h3>i10-index</h3>
        <p id="i10Index">Loading…</p>
    </div>
</div>

<p id="lastUpdated" style="opacity:0.7; font-size:0.9em;"></p>

---

## Citations Over Time

<canvas id="citationsChart" width="400" height="200"></canvas>

---

## Publications

<div class="pub-controls">
    <label>Sort by:</label>
    <select id="sortMode">
        <option value="year">Year (Newest First)</option>
        <option value="citations">Citations (Most First)</option>
        <option value="title">Title (A–Z)</option>
    </select>

    <label style="margin-left:20px;">Filter by year:</label>
    <select id="yearFilter">
        <option value="all">All</option>
    </select>

    <label style="margin-left:20px;">Keyword:</label>
    <input type="text" id="keywordFilter" placeholder="Search title or journal">
</div>

<div id="pubList"></div>

---

## Recent Publications

<div id="recentPubs"></div>

---

## Scripts

<script>
// GLOBAL PUBLICATION LIST (loaded from scholar.json)
let publications = [];

// Load publications from scholar.json
async function loadPublications() {
    const response = await fetch("/assets/data/scholar.json");
    const data = await response.json();

    publications = data.publications.map(p => ({
        title: p.title,
        authors: p.authors,
        journal: p.journal,
        year: Number(p.year),
        citations: p.cited_by,
        doi: p.doi
    }));

    populateYearFilter();
    applyFilters();
    renderRecentPublications();
    buildCoauthorGraph();
}

// Populate year dropdown dynamically
function populateYearFilter() {
    const years = [...new Set(publications.map(p => p.year))]
        .sort((a, b) => b - a);

    const yearFilter = document.getElementById("yearFilter");
    years.forEach(y => {
        const opt = document.createElement("option");
        opt.value = y;
        opt.textContent = y;
        yearFilter.appendChild(opt);
    });
}

// Render full publication list
function renderPublications(list) {
    const container = document.getElementById("pubList");
    container.innerHTML = "";

    list.forEach(pub => {
        container.innerHTML += `
            <div class="pub-card">
                <h3>${pub.title}</h3>
                <p><strong>Authors:</strong> ${pub.authors}</p>
                <p><strong>Journal:</strong> ${pub.journal} (${pub.year})</p>
                <p><span class="badge">Cited by ${pub.citations}</span></p>
                ${pub.doi ? `<a href="https://doi.org/${pub.doi}" target="_blank">View DOI</a>` : `<em>No DOI available</em>`}
            </div>
        `;
    });
}

// Render recent publications (top 5)
function renderRecentPublications() {
    const recent = [...publications]
        .sort((a, b) => b.year - a.year)
        .slice(0, 5);

    const container = document.getElementById("recentPubs");
    container.innerHTML = "";

    recent.forEach(pub => {
        container.innerHTML += `
            <div class="pub-card">
                <h3>${pub.title}</h3>
                <p><strong>${pub.year}</strong> — ${pub.journal}</p>
                <p><span class="badge">Cited by ${pub.citations}</span></p>
                ${pub.doi ? `<a href="https://doi.org/${pub.doi}" target="_blank">View DOI</a>` : ""}
            </div>
        `;
    });
}

// Apply sorting + filtering
function applyFilters() {
    let list = [...publications];

    const sortMode = document.getElementById("sortMode").value;
    if (sortMode === "year") list.sort((a,b) => b.year - a.year);
    if (sortMode === "citations") list.sort((a,b) => b.citations - a.citations);
    if (sortMode === "title") list.sort((a,b) => a.title.localeCompare(b.title));

    const year = document.getElementById("yearFilter").value;
    if (year !== "all") list = list.filter(p => p.year == year);

    const keyword = document.getElementById("keywordFilter").value.toLowerCase();
    if (keyword.length > 0) {
        list = list.filter(p =>
            p.title.toLowerCase().includes(keyword) ||
            p.journal.toLowerCase().includes(keyword)
        );
    }

    renderPublications(list);
}

// Co-author graph
function buildCoauthorGraph() {
    const container = document.getElementById("coauthorGraph");
    if (!container) return;

    const authors = {};
    const links = [];

    publications.forEach(pub => {
        const coauthors = pub.authors.split(",").map(a => a.trim());

        for (let i = 0; i < coauthors.length; i++) {
            for (let j = i + 1; j < coauthors.length; j++) {
                const a = coauthors[i];
                const b = coauthors[j];

                if (!authors[a]) authors[a] = { name: a };
                if (!authors[b]) authors[b] = { name: b };

                let link = links.find(l =>
                    (l.source === a && l.target === b) ||
                    (l.source === b && l.target === a)
                );

                if (link) link.weight += 1;
                else links.push({ source: a, target: b, weight: 1 });
            }
        }
    });

    drawCoauthorGraph(Object.values(authors), links);
}

// Scholar metrics
async function updateScholarMetrics() {
    try {
        const response = await fetch("/assets/data/scholar.json");
        const data = await response.json();

        if (data.metrics) {
            document.getElementById("totalCitations").innerText = data.metrics.total_citations;
            document.getElementById("hIndex").innerText = data.metrics.h_index;
            document.getElementById("i10Index").innerText = data.metrics.i10_index;
        }

        if (data.metrics && data.metrics.citations_per_year) {
            const yearly = Object.entries(data.metrics.citations_per_year)
                .map(([year, citations]) => ({ year, citations }))
                .sort((a, b) => a.year - b.year);

            drawCitationsGraph(yearly);
        }

        document.getElementById("lastUpdated").innerText =
            "Last updated: " + new Date().toLocaleString();

    } catch (e) {
        console.log("Metrics update failed:", e);
    }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    loadPublications();
    updateScholarMetrics();

    document.getElementById("sortMode").onchange = applyFilters;
    document.getElementById("yearFilter").onchange = applyFilters;
    document.getElementById("keywordFilter").onkeyup = applyFilters;
});
</script>
