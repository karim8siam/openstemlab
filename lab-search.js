'use strict';
(()=>{
  // Levenshtein edit distance for typo tolerance
  function lev(a, b) {
    if (a === b) return 0;
    const la = a.length, lb = b.length;
    if (!la) return lb;
    if (!lb) return la;
    if (Math.abs(la - lb) > 2) return 99;
    const d = [];
    for (let i = 0; i <= la; i++) d[i] = [i];
    for (let j = 0; j <= lb; j++) d[0][j] = j;
    for (let i = 1; i <= la; i++) {
      for (let j = 1; j <= lb; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
      }
    }
    return d[la][lb];
  }

  // Suffix stripper for basic English stemming
  function stem(w) {
    return w.replace(/(ing|tion|ment|ness|ity|ous|ive|ed|es|s|al|ic)$/i, '');
  }

  // String normalizer
  const normalize = s => (s || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[’']/g, '')
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .trim();

  // Physics synonyms and typo alias map
  const SYNONYMS = {
    'pendulam': 'pendulum', 'pendulm': 'pendulum', 'pendulums': 'pendulum', 'bob': 'pendulum',
    'gravty': 'gravity', 'graivty': 'gravity', 'freefall': 'free fall', 'falling': 'free fall',
    'boyls': 'boyle', 'boyles': 'boyle', 'boyl': 'boyle',
    'charls': 'charles', 'gaylusac': 'gay lussac', 'gaylussac': 'gay lussac',
    'viscocity': 'viscosity', 'viscous': 'viscosity', 'viscos': 'viscosity',
    'calorimeter': 'calorimetry', 'calorimetr': 'calorimetry',
    'friciton': 'friction', 'frictin': 'friction',
    'diffrection': 'diffraction', 'difraction': 'diffraction',
    'interferance': 'interference', 'interfere': 'interference',
    'vapper': 'vapor', 'vapour': 'vapor', 'evaporation': 'vapor',
    'humidty': 'humidity', 'hygrometr': 'hygrometer', 'psycrometer': 'psychrometer',
    'micrometr': 'micrometer', 'verner': 'vernier', 'caliper': 'calipers',
    'archimeds': 'archimedes', 'dencity': 'density',
    'hook': 'hooke', 'hoke': 'hooke', 'elastic': 'elasticity',
    'photogate': 'photogates', 'projectile': 'ballistic', 'momentum': 'ballistic',
    'heat': 'thermal temperature calorimetry specific latent',
    'optics': 'lens reflection refraction focal convex glass slab grating light',
    'gas': 'boyle charles pressure volume manometer ideal atmosphere',
    'sound': 'resonance tuning fork wavelength frequency',
    'electricity': 'ohm resistance voltage current bridge circuit capacitor'
  };

  for (const root of document.querySelectorAll('[data-lab-search]')) {
    const query = root.querySelector('[data-lab-query]'),
          scope = root.querySelector('[data-lab-scope]'),
          cards = [...root.querySelectorAll('[data-lab-card]')],
          seeMoreWrap = root.querySelector('[data-lab-see-more-wrap]'),
          seeMoreBtn = root.querySelector('[data-lab-see-more]'),
          countEl = root.querySelector('[data-lab-count]'),
          emptyEl = root.querySelector('[data-lab-empty]');

    let visibleLimit = 6;
    let currentMatchedCards = [];

    // Pre-parse cards for fast fuzzy matching
    const cardData = cards.map(c => {
      const searchStr = normalize(c.dataset.search);
      const titleStr = normalize(c.querySelector('h3')?.textContent || '');
      const words = searchStr.split(/\s+/).filter(Boolean);
      const stemmedWords = words.map(stem);
      return { el: c, subject: c.dataset.subject, words, stemmedWords, searchStr, titleStr };
    });

    function scoreCard(card, tokens) {
      if (scope.value !== 'all' && card.subject !== scope.value) return 0;
      if (!tokens.length) return 1;

      let totalScore = 0;
      let matchedTokens = 0;

      for (const rawToken of tokens) {
        const token = SYNONYMS[rawToken] || rawToken;
        const tokenWords = token.split(/\s+/).filter(Boolean);
        let tokenMatched = false;

        for (const subToken of tokenWords) {
          const sToken = stem(subToken);
          // 1. Exact match in title
          if (card.titleStr.includes(subToken)) {
            totalScore += 50;
            tokenMatched = true;
          }
          // 2. Exact word match in keywords/body
          else if (card.words.includes(subToken)) {
            totalScore += 25;
            tokenMatched = true;
          }
          // 3. Substring match
          else if (card.searchStr.includes(subToken)) {
            totalScore += 15;
            tokenMatched = true;
          }
          // 4. Stemmed word match
          else if (card.stemmedWords.includes(sToken)) {
            totalScore += 12;
            tokenMatched = true;
          }
          // 5. Levenshtein fuzzy match
          else {
            const maxDist = subToken.length >= 7 ? 2 : subToken.length >= 4 ? 1 : 0;
            if (maxDist > 0) {
              for (const w of card.words) {
                if (Math.abs(w.length - subToken.length) <= maxDist && lev(w, subToken) <= maxDist) {
                  totalScore += 8;
                  tokenMatched = true;
                  break;
                }
              }
            }
          }
        }
        if (tokenMatched) matchedTokens++;
      }

      if (tokens.length > 1 && matchedTokens === tokens.length) {
        totalScore += 40;
      }

      return matchedTokens > 0 ? totalScore : 0;
    }

    function renderCards() {
      cards.forEach(c => c.hidden = true);

      const toShow = currentMatchedCards.slice(0, visibleLimit);
      toShow.forEach(item => item.el.hidden = false);

      const totalMatches = currentMatchedCards.length;
      emptyEl.hidden = totalMatches > 0;

      const qText = query.value.trim();
      if (!qText && scope.value === 'all') {
        countEl.textContent = `${totalMatches} experiments available (showing ${Math.min(visibleLimit, totalMatches)})`;
      } else {
        countEl.textContent = `${totalMatches} experiment${totalMatches === 1 ? '' : 's'} found${qText ? ' for “' + qText + '”' : ''} (showing ${Math.min(visibleLimit, totalMatches)})`;
      }

      if (seeMoreWrap) {
        if (visibleLimit >= totalMatches) {
          if (totalMatches > 6) {
            seeMoreWrap.hidden = false;
            seeMoreBtn.textContent = 'Show less ↑';
            seeMoreBtn.setAttribute('data-mode', 'less');
          } else {
            seeMoreWrap.hidden = true;
          }
        } else {
          seeMoreWrap.hidden = false;
          const remaining = totalMatches - visibleLimit;
          seeMoreBtn.textContent = `See more experiments (${remaining} more) ↓`;
          seeMoreBtn.setAttribute('data-mode', 'more');
        }
      }
    }

    function filter(resetLimit = true) {
      if (resetLimit) visibleLimit = 6;
      const rawTokens = normalize(query.value).split(/\s+/).filter(Boolean);

      const scored = [];
      for (const card of cardData) {
        const score = scoreCard(card, rawTokens);
        if (score > 0) {
          scored.push({ el: card.el, score });
        }
      }

      if (rawTokens.length > 0) {
        scored.sort((a, b) => b.score - a.score);
        const container = root.querySelector('.experiment-results');
        if (container) {
          scored.forEach(item => container.appendChild(item.el));
        }
      }

      currentMatchedCards = scored;
      renderCards();
    }

    if (seeMoreBtn) {
      seeMoreBtn.onclick = () => {
        if (seeMoreBtn.getAttribute('data-mode') === 'less') {
          visibleLimit = 6;
          root.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          visibleLimit += 6;
          if (visibleLimit >= currentMatchedCards.length) {
            visibleLimit = currentMatchedCards.length;
          }
        }
        renderCards();
      };
    }

    query.addEventListener('input', () => filter(true));
    scope.addEventListener('change', () => filter(true));
    root.querySelector('[data-lab-clear]').onclick = () => { query.value = ''; filter(true); query.focus(); };
    root.querySelector('[data-lab-all]').onclick = () => { scope.value = 'all'; filter(true); query.focus(); };

    filter(true);
  }
})();
