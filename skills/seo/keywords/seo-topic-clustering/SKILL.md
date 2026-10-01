---
name: seo-topic-clustering
description: >-
  Turn a raw keyword list into topic clusters with a pillar page, supporting pages and an internal-linking map, using SERP overlap to decide what shares a page. Use when asked to "cluster these keywords", "group keywords by topic", "build a pillar and cluster plan", "which keywords go on the same page", "content hub structure", or after seo-keyword-research produces a long list.
metadata:
  department: "seo"
  domain: "keywords"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Topic clustering

Clustering decides page count. Too few pages and you fail to match intent; too many and you cannibalise yourself and thin your authority.

## Principle
Two keywords belong on the same page when their SERPs largely return the same URLs. They need separate pages when the SERPs differ. Semantic similarity alone is not enough.

## Workflow
1. **Start from the normalised list** (variants already merged). Each row has a keyword, intent and volume.
2. **Rough-group by theme** by hand or simple text similarity, only to reduce the number of SERP checks.
3. **Validate with SERP overlap.** For each candidate pair compare the top 10 URLs. Rule of thumb: 4 or more shared URLs means one page; 2-3 means judgement (often one page with a distinct section); 0-1 means separate pages. If the team has a clustering tool, use it, then spot-check 10 percent by eye.
4. **Define each cluster:** primary keyword (best intent fit and winnable), secondary keywords sharing the SERP, intent, and target page type.
5. **Build the hierarchy.** Pillar: a broad page covering the whole topic and linking to every sub-topic. Cluster pages: one specific question, use case or comparison each. A cluster with fewer than about 4 supporting pages is usually just one guide.
6. **Assign existing URLs.** Match clusters to current pages first. Mark each: has page (optimise), has page but wrong intent (rebuild), no page (create), duplicate pages (merge and redirect).
7. **Plan internal links.** Every cluster page links up to the pillar with descriptive anchors, the pillar links down to all, and siblings link where one answers the reader's next question. Money pages receive links from relevant informational pages. Record anchor text and placement.
8. **Sequence.** Pillar and commercial pages first, then clusters in the priority order from `seo-keyword-research`. Publish in batches so interlinks exist at launch.

## Output
- Cluster table: cluster | primary keyword | secondary keywords | intent | page type | role (pillar / cluster) | URL status | priority.
- A text tree of pillar to cluster pages.
- Internal link matrix (from, to, anchor).
- Cannibalisation risks found.

## Failure modes
- Clustering by shared words ("accounting software" and "accounting software for restaurants" may need separate pages).
- A pillar that is a thin index of links. It must stand as a full resource.
- Orphaned cluster pages.
- Forcing every keyword into a hub when it has no business link.
