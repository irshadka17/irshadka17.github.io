---
layout: page
title: Publications
---

# Publications

<p>This page loads publication metadata directly from DOIs.  
Update <code>assets/dois.txt</code> to add new papers.</p>

<div id="pub-container">
  <p>Loading publications…</p>
</div>

<script>
// Load DOI list from your site (never navigates away)
async function loadDOIs() {
  const response = await fetch('{{ "/assets/dois.txt" | relative_url }}');
  const text = await response.text();
  return text.split('\n').map(d => d.trim()).filter(d => d.length > 0);
}

// Fetch metadata from CrossRef
async function fetchCrossRef(doi) {
  const url = `https://api.crossref.org/works/${encodeURIComponent(doi)}`;
  const response = await fetch(url);
  return (await response.json()).message;
}

// Fetch citation count from OpenAlex
async function fetchOpenAlex(doi) {
  const url = `https://api.openalex.org/works/doi:${encodeURIComponent(doi)}`;
  const response = await fetch(url);
  const data = await response.json();
  return data.cited_by_count || 0;
}

// Render publication card
function renderPublication(meta, citations) {
  const authors = meta.author
    ? meta.author.map(a => `${a.given} ${a.family}`).join(', ')
    : 'Unknown authors';

  const title = meta.title ? meta.title[0] : 'Untitled';
  const journal = meta['container-title'] ? meta['container-title'][0] : 'Unknown journal';
  const year = meta.issued ? meta.issued['date-parts'][0][0] : '—';
  const doi = meta.DOI;

  return `
    <div class="pub-card">
      <h3>${title}</h3>
      <p><strong>Authors:</strong> ${authors}</p>
      <p><strong>Journal:</strong> ${journal} (${year})</p>
      <p><strong>Citations:</strong> ${citations}</p>
      <p><a href="https://doi.org/${doi}" target="_blank">DOI: ${doi}</a></p>
    </div>
    <hr>
  `;
}

// Main loader
async function loadPublications() {
  const container = document.getElementById('pub-container');
  container.innerHTML = '<p>Loading…</p>';

  const dois = await loadDOIs();
  let html = '';

  for (const doi of dois) {
    try {
      const meta = await fetchCrossRef(doi);
      const citations = await fetchOpenAlex(doi);
      html += renderPublication(meta, citations);
    } catch (err) {
      html += `<p>Error loading DOI ${doi}</p>`;
    }
  }

  container.innerHTML = html;
}

loadPublications();
</script>

<style>
.pub-card {
  margin-bottom: 1.5rem;
}
</style>
