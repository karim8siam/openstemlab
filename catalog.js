'use strict';
const search=document.getElementById('subjectSearch'),cards=[...document.querySelectorAll('.subject-card')],filters=[...document.querySelectorAll('[data-filter]')];
let group='all';function filterSubjects(){const q=search.value.trim().toLocaleLowerCase();let n=0;for(const card of cards){const show=(group==='all'||card.dataset.group===group)&&card.dataset.search.includes(q);card.hidden=!show;if(show)n++;}document.getElementById('resultCount').textContent=n+' subject'+(n===1?'':'s');document.getElementById('emptyCatalog').hidden=n!==0;filters.forEach(b=>{const active=b.dataset.filter===group;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});}
search.addEventListener('input',filterSubjects);filters.forEach(b=>b.addEventListener('click',()=>{group=b.dataset.filter;filterSubjects();}));document.getElementById('clearSearch').onclick=()=>{search.value='';group='all';filterSubjects();search.focus();};filterSubjects();
// Keep links from the previous one-experiment homepage useful.
if(['experiment','apparatus','method','analysis','check'].includes(location.hash.slice(1)))location.replace('/physics/photoelectric-effect/'+location.hash);
