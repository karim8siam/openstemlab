'use strict';
(()=>{
 const normalize=s=>s.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[’']/g,'').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
 for(const root of document.querySelectorAll('[data-lab-search]')){
  const query=root.querySelector('[data-lab-query]'),scope=root.querySelector('[data-lab-scope]'),cards=[...root.querySelectorAll('[data-lab-card]')];
  const filter=()=>{const tokens=normalize(query.value).split(/\s+/).filter(Boolean);let count=0;for(const card of cards){const words=normalize(card.dataset.search);const visible=(scope.value==='all'||card.dataset.subject===scope.value)&&tokens.every(t=>words.includes(t));card.hidden=!visible;if(visible)count++;}root.querySelector('[data-lab-count]').textContent=count+' experiment'+(count===1?'':'s')+(query.value.trim()?' matching “'+query.value.trim()+'”':'');root.querySelector('[data-lab-empty]').hidden=count>0;};
  query.addEventListener('input',filter);scope.addEventListener('change',filter);root.querySelector('[data-lab-clear]').onclick=()=>{query.value='';filter();query.focus();};root.querySelector('[data-lab-all]').onclick=()=>{scope.value='all';filter();query.focus();};filter();
 }
})();
