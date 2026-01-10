---
layout: default
title: Publications
---

# Publications
### Peer Reviewed Journal Publications

<!--
This page loads publication metadata directly from DOIs.
Update assets/dois.txt to add new papers.
-->

<!-- ========================= -->
<!--   ANALYTICS TOP ROW      -->
<!-- ========================= -->

<div id="analytics-row" style="
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 2rem;
">

  <!-- Left: Citation Timeline -->
  <div id="citation-panel" style="
    flex: 1 1 48%;
    min-width: 300px;
  ">
    <canvas id="citationChart"></canvas>
  </div>

  <!-- Right: Coauthor Graph -->
  <div id="coauthor-panel" style="
    flex: 1 1 48%;
    min-width: 300px;
    height: 400px;
    border: 1px solid #ddd;
    border-radius: 6px;
    position: relative;
  ">
    <svg id="coauthorGraph" width="100%" height="100%"></svg>
  </div>

</div>

<!-- ========================= -->
<!--   FILTERS + CONTROLS     -->
<!-- ========================= -->

<div id="controls" style="margin-bottom: 1.5rem;">

  <!-- Search -->
  <label><strong>Search:</strong></label>
  <input type="text" id="searchInput" placeholder="Search title, author, journal…" style="padding: 4px 8px; width: 250px;">

  <!-- Year Filter -->
  <label style="margin-left: 1rem;"><strong>Year:</strong></label>
  <select id="yearFilter">
    <option value="all">All Years</option>
  </select>

  <!-- Sort -->
  <label style="margin-left: 1rem;"><strong>Sort by:</strong></label>
  <select id="sortSelect">
    <option value="year-desc">Year (newest first)</option>
    <option value="year-asc">Year (oldest first)</option>
    <option value="citations-desc">Citations (high → low)</option>
    <option value="citations-asc">Citations (low → high)</option>
    <option value="title-asc">Title (A → Z)</option>
    <option value="title-desc">Title (Z → A)</option>
  </select>

</div>

<!-- ========================= -->
<!--   PUBLICATION LIST       -->
<!-- ========================= -->

<div id="pub-container">
  <p>Loading publications…</p>
</div>

<!-- ========================= -->
<!--   JS LIBRARIES           -->
<!-- ========================= -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://d3js.org/d3.v7.min.js"></script>

<!-- ========================= -->
<!--   MAIN PUBLICATIONS JS   -->
<!-- ========================= -->

<script src="{{ '/assets/js/publications.js' | relative_url }}"></script>

<style>
.pub-card {
  margin-bottom: 1.5rem;
}

#controls select,
#controls input {
  padding: 4px 8px;
}

#analytics-row {
  margin-bottom: 2rem;
}

#coauthor-panel {
  background: #fafafa;
}
</style>
