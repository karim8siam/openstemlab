"""Public experiment directory and reusable department-aware search."""
import json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def experiment_index(experiments):
 configs={c['slug']:c for c in json.loads((ROOT/'content/physics/experiments.json').read_text())}
 if (ROOT/'content/cs/experiments.json').exists():
  configs.update({c['slug']:c for c in json.loads((ROOT/'content/cs/experiments.json').read_text())})
 if (ROOT/'content/chemistry/experiments.json').exists():
  configs.update({c['slug']:c for c in json.loads((ROOT/'content/chemistry/experiments.json').read_text())})
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
   'magnetic-fields':'magnetic fields tangent galvanometer biot savart law circular coil earth horizontal magnetic component reduction factor compass needle dip needle helmholtz commutator pohl deflection',
   'electric-fields':'electric fields equipotential mapping lines potential gradient teledeltos paper conducting sheet parallel plates dipole concentric electrodes laplace equation voltmeter probe',
   'magnetic-moments':'magnetic moments deflection magnetometer gauss tan-a tan-b end on broadside dipole moment inverse cube law vibration magnetometer oscillation period bar magnet alnico compass needle',
   'internal-resistance':'internal resistance electromotive force emf terminal voltage potential difference cell battery decade resistance box voltmeter ammeter maximum power transfer load current short circuit',
   'temperature-resistance':'temperature coefficient resistance rtd copper coil thermometer wheatstone bridge kelvin callendar van dusen drude model electron phonon scattering heating bath ice point',
   'faradays-law-electrolysis':'faraday law electrolysis electrochemical equivalent copper voltameter deposition cathode anode charge coulomb avogadro constant molar mass chemical equivalent',
    'electrical-equivalent-heat':'electrical equivalent heat joule law heating calorimeter immersion coil water equivalent rumford cooling electric power energy conservation nichrome resistance chronometer',
    'potentiometer-emf-comparison':'potentiometer slide wire electromotive force emf weston standard cell null balance galvanometer jockey poggendorff potential gradient volt comparison internal resistance dry cell',
    'emission-spectra-spectroscopy':'emission spectra spectroscopy balmer series rydberg constant hydrogen geissler tube diffraction grating bohr atom quantum energy levels fraunhofer lines wavelength wavenumber',
    'photometry-lamp-efficiency':'photometry lamp efficiency lummer brodhun bunsen grease spot candela lumen lux illuminance inverse square law luminous efficacy incandescent cfl led photometer bench optical track',
    'search-algorithms-complexity':'binary search linear search interpolation search time complexity asymptotic analysis big-o logarithm divide and conquer array decision tree algorithm profiling',
    'quadratic-sorting-algorithms':'bubble sort selection sort insertion sort quadratic sorting algorithms time complexity inversions swaps memory writes stability permutation comparison count',
    'divide-conquer-sorting':'merge sort quick sort heap sort divide and conquer recursion tree master theorem introsort timsort comparisons auxiliary space stability cache locality decision tree lower bound',
    'stack-adt-recursion':'stack abstract data type lifo recursion call stack activation record stack frame rsp rbp memory consumption overflow shunting yard parentheses parsing tail call optimization',
    'queue-buffer-management':'queue abstract data type fifo circular ring buffer modular arithmetic producer consumer false sharing cache line padding backpressure disruptor socket buffer pipe',
    'linked-list-architectures':'linked list doubly singly pointer hopping cache locality spatial prefetcher sentinel dummy node unrolled list intrusive list container_of dynamic memory fragmentation',
    'binary-search-trees':'binary search tree bst tree height balance factor avl red black tree rotations b-tree degeneracy internal path length search depth',
    'binary-heaps-priority-queues':'binary heap priority queue max heap min heap floyd build_heap sift down sift up heapsort d-ary heap 4-way heap dijkstra scheduler',
    'hash-tables-collision-resolution':'hash table collision resolution separate chaining open addressing linear probing quadratic probing double hashing load factor clustering swiss table robin hood knuth probe length',
    'graph-traversal-shortest-paths':'graph traversal breadth first search depth first search bfs dfs dijkstra shortest path adjacency matrix adjacency list compressed sparse row csr edge relaxation priority queue',
    'dynamic-programming-memoization':'dynamic programming memoization tabulation bellman recurrence optimal substructure overlapping subproblems 0 1 knapsack state space pseudo polynomial weak np complete rolling array reverse scan',
    'greedy-minimum-spanning-trees':'greedy algorithm minimum spanning tree mst kruskal prim boruvka disjoint set union dsu union find path compression union by rank cut property cycle property matroid',
    'string-matching-automata':'string matching automata knuth morris pratt kmp failure function prefix array boyer moore bad character good suffix rabin karp rolling hash aho corasick trie simd avx512',
    'network-flow-max-cut':'network flow maximum flow max cut min cut ford fulkerson edmonds karp dinic push relabel residual graph augmenting path bottleneck capacity level graph bipartite matching duality',
    'trie-prefix-trees':'trie prefix tree radix tree patricia compressed ternary search tree tst longest prefix matching lpm cidr routing adaptive radix tree art suffix tree',
    'huffman-coding-compression':'huffman coding data compression lossless shannon entropy kraft mcmillan prefix property min heap greedy canonical huffman deflate gzip lz77 arithmetic coding bitstream bit packing',
    'computational-geometry-convex-hull':'computational geometry convex hull graham scan jarvis march gift wrapping quickhull chan output sensitive 2d cross product counter clockwise ccw determinant orientation predicate shewchuk robust',
    'backtracking-n-queens-sat':'backtracking constraint satisfaction csp n-queens sat solver boolean satisfiability dpll cdcl conflict driven clause learning implication graph 1uip unit propagation boolean constraint propagation bcp pure literal two watched literals 2wl vsids state space search tree bitmask two complement',
    'b-tree-disk-indexing':'b-tree b+ tree external memory disk indexing disk access machine dam block io 4kb page buffer pool lru fanout binary search multi-way balanced tree node split write ahead logging wal aries in-node binary search',
    'concurrency-synchronization-deadlock':'concurrency synchronization deadlock mutex lock counting semaphore dining philosophers problem coffman conditions resource allocation graph rag bankers algorithm dijkstra race condition critical section peterson algorithm compare and swap cas test and set atomic lock free thread safety starvation priority inversion',
    'cryptographic-rsa-modular':'cryptographic rsa modular arithmetic public key cryptography encryption decryption square and multiply modular exponentiation extended euclidean algorithm bezout identity modular inverse euler totient phi miller rabin primality test prime factorization gnfs shor algorithm asymmetric key exchange',
    'lru-cache-replacement':'lru cache page replacement least recently used second chance clock algorithm fifo first in first out belady anomaly optimal page replacement min working set denning temporal locality spatial locality doubly linked hash map cache miss hit ratio effective memory access time emat virtual memory os operating system',
    'a-star-pathfinding-heuristics':'a star a* pathfinding heuristic search admissible consistent manhattan euclidean chebyshev octile open set closed set priority queue min heap edge relaxation state space exploration dijkstra greedy best first jump point search jps ida* shortest path graph navigation',
    'fast-fourier-transform':'fast fourier transform fft cooley tukey radix-2 decimation in time dit butterfly operation twiddle factor roots of unity bit reversal permutation convolution theorem polynomial multiplication frequency domain spectral analysis discrete fourier transform dft ifft signal processing',
    'relational-query-optimization':'relational query optimization execution relational algebra equivalence predicate pushdown projection pruning cost-based join nested loop block nested loop index nested loop sort merge join hash join grace hash join selinger dynamic programming system r left deep tree interesting order cardinality estimation selectivity histogram tipping point b+ tree index scan buffer pool',
    'density-mass-volume-precision':'precision density determination analytical balance volumetric pycnometry burette pipette water buoyancy correction archimedes mass volume least squares regression metrology',
    'hydrate-stoichiometric-composition':'gravimetric stoichiometry hydrated salts thermal dehydration water crystallization empirical formula copper sulfate pentahydrate crucible desiccator tga jahn teller crystal field',
    'limiting-reactant-precipitation':'limiting reactant gravimetric stoichiometry precipitation barium sulfate percentage yield ostwald ripening von weimarn supersaturation gooch crucible silver nitrate test buchner vacuum filtration',
    'molar-volume-ideal-gas':'molar volume ideal gas eudiometer acid metal displacement magnesium hydrogen gas dalton partial pressure water vapor pressure leveling cylinder stp avogadro van der waals',
    'volatile-liquid-molar-mass':'molar mass volatile liquid dumas method vapor density cyclohexane boiling water bath pinhole air buoyancy pycnometry ideal gas equation of state van der waals',
    'chemical-reactions-copper-cycle':'chemical reactions copper cycle conservation of mass redox metathesis precipitation dehydration neutralization single displacement gravimetric recovery percentage yield lavoisier stoichiometry tenorite',
    'empirical-formula-magnesium-oxide':'empirical formula magnesium oxide crucible thermal oxidation meker burner porcelain constant mass proust definite proportions dalton magnesium nitride hydrolysis ammonia steam rocksalt lattice',
    'liquid-viscosity-poiseuille':'liquid dynamic viscosity hagen poiseuille capillary flow hydrostatic head water jacket newton shear stress laminar reynolds number ostwald falling sphere rotational couette',
    'surface-tension-stalagmometry':'surface tension drop weight stalagmometry traube tate law harkins jordan correction rayleigh plateau neck pinch off du nouy ring wilhelmy plate capillary rise interfacial thermodynamics',
    'colligative-freezing-point-depression':'colligative properties freezing point depression cryoscopy beckmann differential thermometer cyclohexane biphenyl raoult law chemical potential plastic crystal supercooling latent heat fusion ebulliometry osmometry',
    'solution-calorimetry-neutralization':'solution calorimetry enthalpy of neutralization acid base dewar dewar flask thermistor thermochemistry hess law heat of reaction hydronium hydroxide strong acid strong base adiabatic temperature rise cooling curve heat capacity',
    'hess-law-magnesium-calorimetry':'hess law thermochemistry magnesium oxide enthalpy of formation calorimetry dewar state function thermochemical cycle regnault pfaundler adiabatic extrapolation heat of reaction enthalpy change standard enthalpy',
    'combustion-bomb-calorimetry-benzoic':'bomb calorimetry oxygen bomb benzoic acid heat of combustion internal energy enthalpy of combustion thermochemistry parr calorimeter fuse wire water equivalent nist standard constant volume',
    'heat-solution-crystallization-calorimetry':'heat of solution integral heat differential heat potassium nitrate kno3 endothermic dissolution solution calorimetry dewar lattice energy hydration enthalpy van t hoff solubility refrigeration',
    'vapor-pressure-liquid-clausius-clapeyron':'clausius clapeyron vapor pressure enthalpy of vaporization ethanol boiling point isoteniscope liquid vapor equilibrium clapeyron equation trouton rule antoine phase transition',
    'gibbs-free-energy-solubility-van-t-hoff':'van t hoff solubility gibbs free energy enthalpy entropy borax disodium tetraborate decahydrate titration ksp solubility product equilibrium constant debye huckel bromocresol green',
    'heat-capacity-ratio-gases-clement-desormes':'clement desormes heat capacity ratio adiabatic expansion isentropic index gamma cp cv degrees of freedom equipartition ruchhardt carboy manometer gas dynamics',
    'partial-molar-volume-binary-mixtures':'partial molar volume apparent molar volume binary mixtures ethanol water pycnometry gay lussac density excess volume gibbs duhem infinite dilution hydrophobic hydration',
    'liquid-vapor-phase-equilibrium-azeotrope':'liquid vapor equilibrium phase diagram azeotropic distillation azeotrope ethanol water othmer still cottrell pump abbe refractometer margules activity coefficient relative volatility',
    'three-component-liquid-liquid-ternary-phase':'three component ternary liquid phase equilibrium liquid extraction binodal curve tie lines plait point water acetic acid chloroform nernst christian distribution dimerization constant'}
 for exp in experiments:
  c=configs.get(exp['slug'],{})
  if '/computer-science/' in exp.get('page_path',''):
   sub='computer-science'
   sub_name='Computer Science'
  elif '/chemistry/' in exp.get('page_path',''):
   sub='chemistry'
   sub_name='Chemistry'
  else:
   sub='physics'
   sub_name='Physics'
  index.append({'slug':exp['slug'],'title':c.get('title',exp['title']),'subject':sub,'subjectName':sub_name,'path':exp['page_path'],'summary':c.get('aim','Determine Planck’s constant from stopping potential and frequency.'),'keywords':' '.join([aliases.get(exp['slug'],''),*[a['name'] for a in c.get('apparatus',[])]])})
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
