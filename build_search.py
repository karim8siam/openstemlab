"""Public experiment directory and reusable department-aware search."""
import json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def experiment_index(experiments):
 configs={c['slug']:c for c in json.loads((ROOT/'content/physics/experiments.json').read_text())}
 index=[]
 aliases={'simple-pendulum':'gravity g oscillation bob string time period','bifilar-suspension':'rotation inertia rod oscillation strings','young-modulus':'youngs modulus elasticity stress strain wire stretching','stokes-viscosity':'stokes law fluid liquid sphere terminal velocity','convex-lens':'optics focal length lens image uv method','photoelectric-effect':'photon light planck constant stopping potential work function','ohms-law':'ohm ohms law current voltage resistor resistance circuit ammeter voltmeter','metre-bridge':'meter metre wheatstone bridge null galvanometer unknown resistance','rc-charging':'capacitor capacitance resistor rc charge time constant exponential','glass-slab':'refraction refractive index apparent real depth glass microscope','diffraction-grating':'diffraction interference grating spectrum wavelength laser light','hookes-law':'hooke hookes law spring constant stiffness elasticity elongation extension load force','density-measurement':'density mass volume archimedes copper displacement solid balance cylinder','vernier-micrometer':'vernier caliper micrometer screw gauge least count zero error pi circumference diameter length measurement metrology','friction-laws':'friction laws amontons coulomb sliding kinetic static normal force coefficient dynamometer','principle-of-moments':'principle moments torque center gravity lever parallel forces fulcrum meter rule rotational equilibrium balance steelyard','force-table':'force table concurrent forces vector addition resultant equilibrant components pulleys ring equilibrium parallelogram law','equilibrium-forces':'parallel forces non-concurrent rigid body equilibrium beam reactions dynamometers support moments translational rotational static equilibrium',
  'free-fall':'free fall acceleration gravity g spark timer drop tower kinematics uniformly accelerated motion plummet photogate',
  'newtons-second-law':'newton second law motion force mass acceleration fletcher trolley dynamics air track photogate',
  'ballistic-pendulum':'ballistic pendulum momentum conservation inelastic collision projectile velocity kinetic energy spring gun',
  'conical-pendulum':'conical pendulum uniform circular motion centripetal force gravity angle period revolution governor watt',
  'flywheel-inertia':'flywheel moment of inertia rotational acceleration dynamics torque angular acceleration drum cord',
  'specific-heat-capacity':'specific heat capacity method mixtures calorimeter heat thermal energy copper water equivalent thermodynamics',
  'newtons-cooling':'newtons law cooling thermal radiation rate decay temperature heat loss calorimeter water jacket',
  'solidification-cooling':'solidification cooling latent heat fusion salol phase change crystalline amorphous wax melting freezing plateau supercooling',
  'latent-heat-vaporization':'latent heat vaporization steam condensation water trap boiler calorimeter phase change enthalpy heat of transformation',
  'latent-heat-fusion':'latent heat fusion ice melting calorimeter method mixtures enthalpy water equivalent phase change rumford radiation',
  'thermal-expansion':'thermal linear expansion dilatometer micrometer screw gauge electric contact copper rod steam jacket coefficient alpha elongation dilatation',
  'mechanical-equivalent-heat':'mechanical equivalent heat joule constant friction drum calorimeter callendar rowland mechanical work torque revolution counter thermal energy',
  'boyles-law':'boyle law isothermal ideal gas pressure volume reciprocal volume mercury manometer j tube pv constant compressibility',
  'charles-law-volume':'charles law gay lussac volume thermal expansion constant pressure gas thermometer dilatometer absolute zero beta coefficient',
   'charles-law-pressure':'charles law gay lussac pressure thermal expansion coefficient constant volume air thermometer jolly bulb absolute zero pressure temperature',
   'vapor-pressure':'saturated vapor pressure enthalpy vaporization volatile liquid ethanol clausius clapeyron boiling point manometer mercury phase equilibrium temperature',
   'air-humidity':'atmospheric humidity psychrometer hygrometer wet dry bulb depression dew point water vapor relative humidity sprung ferrel regnault',
   'loaded-spring':'loaded helical spring simple harmonic motion shm oscillation period rayleigh effective mass spring constant stiffness hooke law slotted weights',
   'pendulum-coincidence':'pendulum coincidence method master seconds clock simple harmonic motion gravity g beat frequency cathetometer border vernier time',
   'torsion-pendulum':'torsion pendulum shear modulus rigidity wire twisting inertia disc coulomb cavendish torque rotational harmonic oscillation',
   'resonance-air-column':'resonance tube air column speed of sound acoustic standing waves water reservoir tuning fork end correction helmholtz wavelength frequency sound velocity node antinode',
   'modes-air-column':'modes vibration air column open closed organ pipe harmonics overtones siren disk acoustic standing waves dual end correction helmholtz rayleigh sound speed',
   'vibration-strings-sonometer':'sonometer vibration strings mersenne laws transverse wave velocity tension linear mass density soundboard paper rider tuning fork beats unison',
   'interference-sound-waves':'kundt tube standing waves air sound velocity metal rod dust heaps lycopodium cork dust wavelength longitudinal waves resonance rod clamp young modulus specific heat ratio',
   'electrostatics':'electrostatics coulomb law electric charge induction gold leaf electroscope faraday ice pail proof plane permittivity electric field torsion balance repulsion dielectric',
   'magnetic-fields':'magnetic fields tangent galvanometer biot savart law circular coil earth horizontal magnetic component reduction factor compass needle dip needle helmholtz commutator pohl deflection'}
 for exp in experiments:
  c=configs.get(exp['slug'],{});index.append({'slug':exp['slug'],'title':c.get('title',exp['title']),'subject':'physics','subjectName':'Physics','path':exp['page_path'],'summary':c.get('aim','Determine Planck’s constant from stopping potential and frequency.'),'keywords':' '.join([aliases.get(exp['slug'],''),*[a['name'] for a in c.get('apparatus',[])]])})
 return index

def search_section(index,subjects,scope='all',heading='Find an experiment',prefix='labs'):
 options='<option value="all"'+(' selected' if scope=='all' else '')+'>All departments</option>'+''.join('<option value="'+E(s['slug'])+'"'+(' selected' if s['slug']==scope else '')+'>'+E(s['name'])+'</option>' for s in subjects)
 cards=''
 for lab in index:
  hidden=scope!='all' and lab['subject']!=scope
  terms=' '.join(['laboratory lab experiment simulation',lab['title'],lab['subjectName'],lab['summary'],lab['keywords']])
  cards+='<article class="experiment-result" data-lab-card data-subject="'+lab['subject']+'" data-search="'+E(terms)+'"'+(' hidden' if hidden else '')+'><span class="eyebrow">'+lab['subjectName']+' · AVAILABLE NOW</span><h3><a href="'+lab['path']+'">'+E(lab['title'])+' ↗</a></h3><p>'+E(lab['summary'])+'</p><div class="experiment-result-links"><a href="'+lab['path']+'">Simulation</a><a href="'+lab['path']+'theory/">Theory</a><a href="'+lab['path']+'report/">Example report</a></div></article>'
 count=sum(scope=='all' or x['subject']==scope for x in index)
 return '<section class="experiment-search" data-lab-search id="'+prefix+'"><div class="catalog-heading"><div><span class="eyebrow">SEARCH THE OPEN LAB</span><h2>'+E(heading)+'</h2></div><a class="back-link" href="/experiments/">Browse every experiment ↗</a></div><p class="section-intro">Search by experiment, topic or apparatus. Choose a department, or search across all departments. Only completed lessons appear here.</p><div class="experiment-search-controls"><div><label for="'+prefix+'-query">Search experiments</label><input id="'+prefix+'-query" data-lab-query type="search" placeholder="Try pendulum, resistance, lens or microscope…" autocomplete="off"></div><div><label for="'+prefix+'-scope">Department</label><select id="'+prefix+'-scope" data-lab-scope>'+options+'</select></div><button class="filter" data-lab-clear type="button">Clear search</button></div><p class="lab-result-count" data-lab-count role="status" aria-live="polite">'+str(count)+' experiments</p><div class="experiment-results">'+cards+'</div><div class="lab-see-more-wrap" data-lab-see-more-wrap><button class="lab-see-more-btn" data-lab-see-more type="button">See more experiments ('+str(max(0,count-6))+' more) ↓</button></div><div class="catalog-empty" data-lab-empty'+(' hidden' if count else '')+'><h3>No completed experiments match this search.</h3><p>Try fewer words or search all departments. Other collections are still being prepared.</p><button class="primary" data-lab-all type="button">Search all departments</button></div><noscript><p>Live filtering requires JavaScript. Use the lesson links above or browse <a href="/experiments/">all experiments</a>.</p></noscript></section>'

def build_directory(out,base,production,index,subjects,head,header,footer):
 target=out/'experiments';target.mkdir(exist_ok=True)
 text=head('/experiments/','Physics & STEM Experiments: Search the Virtual Lab | Open STEM Lab','Find completed university lab experiments by department, topic or apparatus, with simulations, theory, methods and worked reports.',base,production)+'<body><div class="wrap">'+header()+'<main><section class="subject-hero"><span class="eyebrow">THE EXPERIMENT LIBRARY</span><h1>Search the laboratory.</h1><p>Find a practical you are studying, explore its theory, and collect your own virtual observations.</p></section>'+search_section(index,subjects,heading='What would you like to investigate?')+'</main>'+footer()+'</div><script src="/lab-search.js"></script></body></html>'
 (target/'index.html').write_text(text)
 (out/'experiments.json').write_text(json.dumps(index,ensure_ascii=False))
 (out/'lab-search.js').write_text((ROOT/'content/lab-search.js').read_text())
 return '/experiments/'
