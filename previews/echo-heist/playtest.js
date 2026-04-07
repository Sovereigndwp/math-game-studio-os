#!/usr/bin/env node
/**
 * Echo Heist — Pass 2 Playtest Simulation
 * Validates all Pass 1 + Pass 2 systems headlessly.
 */
const fs = require('fs');
const path = require('path');

// ── DOM/Canvas stubs ──────────────────────────────────────────
const stubEl = () => ({ style:{display:'',setProperty(){}}, className:'', textContent:'', value:'', innerHTML:'', focus(){}, addEventListener(){} });
global.document = { getElementById: () => stubEl(), addEventListener(){} };
global.requestAnimationFrame = () => {};
global.window = { AudioContext: class { createOscillator(){return{type:'',frequency:{value:0},connect(){},start(){},stop(){}}} createGain(){return{gain:{value:0,linearRampToValueAtTime(){}},connect(){}}} get destination(){return{}} }, webkitAudioContext: undefined };
const ctxStub = new Proxy({},{get(t,p){if(p==='createRadialGradient')return()=>({addColorStop(){}});return function(){}},set(){return true}});
const canvasStub = {width:960,height:640,getContext:()=>ctxStub};
global.document.getElementById = (id) => id === 'game' ? canvasStub : stubEl();

// ── Load game ─────────────────────────────────────────────────
const html = fs.readFileSync(path.join(__dirname,'current.html'),'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
const code = m[1] + `\nmodule.exports={STATE,MISSIONS,LEVELS,CLASSES,TILE,COLS,ROWS,T,DISTRICT_CONFIG,
ECHO_DURATION,VAULT_TIME_LIMIT,GADGET_DELAY,GADGET_DURATION,
get gameState(){return gameState},set gameState(v){gameState=v},
get selectedClass(){return selectedClass},set selectedClass(v){selectedClass=v},
get currentMission(){return currentMission},set currentMission(v){currentMission=v},
get player(){return player},get guards(){return guards},get cameras(){return cameras},
get interactables(){return interactables},get lootPos(){return lootPos},
get heat(){return heat},set heat(v){heat=v},get noise(){return noise},set noise(v){noise=v},
get score(){return score},set score(v){score=v},get mathCorrect(){return mathCorrect},get mathTotal(){return mathTotal},
get missionTimer(){return missionTimer},set missionTimer(v){missionTimer=v},
get vaultActive(){return vaultActive},get vaultStep(){return vaultStep},get vaultPrompts(){return vaultPrompts},
get escapeActive(){return escapeActive},get escapeCountdown(){return escapeCountdown},set escapeCountdown(v){escapeCountdown=v},
get level(){return level},get mathActive(){return mathActive},get mathPrompt(){return mathPrompt},
get echoAvailable(){return echoAvailable},get echoRecording(){return echoRecording},
get abilityCooldown(){return abilityCooldown},set abilityCooldown(v){abilityCooldown=v},
get abilityBuffType(){return abilityBuffType},get abilityBuffTimer(){return abilityBuffTimer},
get abilityActive(){return abilityActive},get abilityBuffData(){return abilityBuffData},
get gadgetAvailable(){return gadgetAvailable},get gadgetPos(){return gadgetPos},
get gadgetEmitting(){return gadgetEmitting},get gadgetTimer(){return gadgetTimer},
get totalHintsUsed(){return totalHintsUsed},get currentHintsUsed(){return currentHintsUsed},
loadLevel,updatePlayer,updateGuard,updateCamera,updateEcho,updateEscape,
startVault,advanceVault,finishVault,startEscape,
startEchoRecording,stopEchoRecording,
tryInteract,openMathPopup,closeMathPopup,checkAnswer,tileAt,isSolid,pixelToGrid,finishMission,
handleMenuKey,handleBriefingKey,handlePlayingKey,handleMathKey,handleVaultKey,handleResultsKey,
activateAbility,resolveAbility,placeGadget,showHint,
getDistrict,getDConfig,generateLevel,
keys};`;
const tmp = path.join(__dirname,'_pt2_tmp.js');
fs.writeFileSync(tmp,code);
let G;
try { G = require(tmp); } catch(e) { console.error('Load failed:',e.message); fs.unlinkSync(tmp); process.exit(1); }
fs.unlinkSync(tmp);

// ── Helpers ───────────────────────────────────────────────────
let passed=0, failed=0;
function assert(c,msg){if(c){passed++;console.log(`  ✓ ${msg}`)}else{failed++;console.error(`  ✗ FAIL: ${msg}`)}}
function simKey(key){const e={key,preventDefault(){}};G.keys[key.toLowerCase()]=true;
if(G.gameState===G.STATE.VAULT)G.handleVaultKey(e);else if(G.gameState===G.STATE.MATH)G.handleMathKey(e);
else if(G.gameState===G.STATE.MENU)G.handleMenuKey(e);else if(G.gameState===G.STATE.BRIEFING)G.handleBriefingKey(e);
else if(G.gameState===G.STATE.RESULTS||G.gameState===G.STATE.CAUGHT)G.handleResultsKey(e);
else if(G.gameState===G.STATE.PLAYING)G.handlePlayingKey(e);G.keys[key.toLowerCase()]=false}
function typeAns(ans){const inp=stubEl();inp.value=ans;const orig=global.document.getElementById;
global.document.getElementById=(id)=>{if(id==='popup-input')return inp;if(id==='game')return canvasStub;return stubEl()};
simKey('Enter');global.document.getElementById=orig}
function moveTo(tx,ty){G.player.x=tx*G.TILE+G.TILE/2;G.player.y=ty*G.TILE+G.TILE/2}
function safeGuards(){G.guards.forEach(g=>{g.state='patrol';g.x=G.TILE;g.y=14*G.TILE});G.heat=0}

// ═══════════════════════════════════════════════════════════════
console.log('\n═══════════════════════════════════════════');
console.log('  ECHO HEIST — Pass 2 Full Playtest');
console.log('═══════════════════════════════════════════\n');

// ── 1. Content validation ──
console.log('1. CONTENT VALIDATION');
assert(G.MISSIONS.length === 30, `30 missions loaded (got ${G.MISSIONS.length})`);
assert(G.LEVELS.length === 30, `30 levels loaded (got ${G.LEVELS.length})`);
assert(G.MISSIONS[0].district === 'Training Gallery', 'Mission 1 is District 1');
assert(G.MISSIONS[10].district === 'Camera Commons', 'Mission 11 is District 2');
assert(G.MISSIONS[20].district === 'Escape Lines', 'Mission 21 is District 3');
for (let i = 0; i < 30; i++) {
  const mi = G.MISSIONS[i];
  assert(mi.prompts.length >= 5, `Mission ${i+1} has ${mi.prompts.length} prompts`);
  assert(mi.vaultPrompts.length >= 2, `Mission ${i+1} has ${mi.vaultPrompts.length} vault prompts`);
  assert(mi.escapePrompts.length >= 1, `Mission ${i+1} has escape prompt`);
  const lv = G.LEVELS[i];
  assert(lv.map.length === G.ROWS, `Level ${i+1} map ok`);
  assert(lv.guards.length >= 2, `Level ${i+1} guards: ${lv.guards.length}`);
}

// ── 2. District config ──
console.log('\n2. DISTRICT CONFIG');
assert(G.DISTRICT_CONFIG.length === 3, '3 district configs');
assert(G.getDistrict(0) === 0 && G.getDistrict(10) === 1 && G.getDistrict(25) === 2, 'District mapping correct');
assert(G.DISTRICT_CONFIG[0].escapeTime === 60, 'D1 escape 60s');
assert(G.DISTRICT_CONFIG[1].escapeTime === 50, 'D2 escape 50s');
assert(G.DISTRICT_CONFIG[2].escapeTime === 45, 'D3 escape 45s');

// ── 3. Class abilities ──
console.log('\n3. CLASS ABILITIES');
simKey('Enter'); simKey('Enter'); // menu→briefing→playing
assert(G.gameState === G.STATE.PLAYING, 'In PLAYING');
G.activateAbility();
assert(G.abilityActive, 'Ability popup opened');
const abilityAns = G.mathPrompt.answer;
typeAns(abilityAns);
G.closeMathPopup(true);
assert(!G.abilityActive, 'Ability resolved');
assert(G.abilityCooldown > 0, `Cooldown: ${G.abilityCooldown}s`);
assert(G.abilityBuffType === 'overclock', 'Hacker → overclock buff');

// ── 4. Gadget ──
console.log('\n4. GADGET');
assert(G.gadgetAvailable, 'Available');
G.placeGadget();
assert(!G.gadgetAvailable, 'Used');
assert(G.gadgetPos !== null, 'Placed');
for (let i = 0; i < 150; i++) G.updatePlayer(0.016);
assert(G.gadgetEmitting, 'Emitting after delay');
for (let i = 0; i < 300; i++) G.updatePlayer(0.016);
assert(!G.gadgetEmitting, 'Stopped');

// ── 5. Hints ──
console.log('\n5. HINTS');
safeGuards();
const ia0 = G.interactables[0];
moveTo(ia0.gx, ia0.gy);
simKey('e');
assert(G.gameState === G.STATE.MATH, 'Popup for hint test');
const sb = G.score;
G.showHint();
assert(G.currentHintsUsed === 1, 'Hint 1');
assert(G.score < sb, 'Score reduced');
G.showHint();
assert(G.currentHintsUsed === 2, 'Hint 2');
G.showHint();
assert(G.currentHintsUsed === 2, 'Capped at 2');
typeAns(ia0.prompt.answer);
G.closeMathPopup(true);

// ── 6. Full mission 1 ──
console.log('\n6. FULL MISSION 1');
G.currentMission = 0; G.loadLevel(0); G.gameState = G.STATE.PLAYING;
for (const ia2 of G.interactables) { moveTo(ia2.gx,ia2.gy); safeGuards(); simKey('e'); if(G.gameState===G.STATE.MATH){typeAns(ia2.prompt.answer);G.closeMathPopup(true)} }
G.startVault();
for (const vp of G.MISSIONS[0].vaultPrompts) { typeAns(vp.answer); G.advanceVault(); }
assert(G.escapeActive, 'Escape after vault');
const eg = G.interactables.find(i2=>i2.type==='escape_gate'&&!i2.solved);
if(eg){moveTo(eg.gx,eg.gy);safeGuards();simKey('e');if(G.gameState===G.STATE.MATH){typeAns(G.MISSIONS[0].escapePrompts[0].answer);G.closeMathPopup(true)}}
moveTo(21,12); G.finishMission();
assert(G.gameState === G.STATE.RESULTS, 'Complete');
console.log(`  Score: $${G.score}`);

// ── 7. District 2 ──
console.log('\n7. DISTRICT 2');
G.currentMission = 12; G.selectedClass = 'ghost'; G.loadLevel(12); G.gameState = G.STATE.PLAYING;
assert(G.guards.length >= 3, `D2 guards: ${G.guards.length}`);
assert(G.escapeCountdown === 50, `D2 escape: ${G.escapeCountdown}s`);
G.abilityCooldown = 0; G.noise = 50;
G.activateAbility();
typeAns(G.mathPrompt.answer);
G.closeMathPopup(true);
assert(G.noise < 50, `Soft Step: 50 → ${G.noise}`);

// ── 8. District 3 ──
console.log('\n8. DISTRICT 3');
G.currentMission = 25; G.selectedClass = 'runner'; G.loadLevel(25); G.gameState = G.STATE.PLAYING;
assert(G.guards.length >= 4, `D3 guards: ${G.guards.length}`);
assert(G.escapeCountdown === 45, `D3 escape: ${G.escapeCountdown}s`);
G.abilityCooldown = 0;
G.activateAbility();
typeAns(G.mathPrompt.answer);
G.closeMathPopup(true);
assert(G.abilityBuffType === 'burst', 'Runner burst');

// ── 9. Procedural level quality ──
console.log('\n9. PROCEDURAL LEVELS');
for (let i = 3; i < 30; i++) {
  const lv = G.LEVELS[i];
  let hasSpawn=false, hasExit=false;
  for (let y=0;y<G.ROWS;y++) for(let x=0;x<G.COLS;x++){if(lv.map[y][x]===G.T.SPAWN)hasSpawn=true;if(lv.map[y][x]===G.T.EXIT)hasExit=true}
  assert(hasSpawn && hasExit, `Level ${i+1}: spawn+exit present`);
}

// ── 10. Math validation ──
console.log('\n10. MATH VALIDATION');
assert(G.checkAnswer('4','4'), 'Integer');
assert(G.checkAnswer('0.5','1/2'), 'Equiv');
assert(!G.checkAnswer('5','4'), 'Reject');

// ═══════════════════════════════════════════════════════════════
console.log('\n═══════════════════════════════════════════');
console.log(`  RESULTS: ${passed} passed, ${failed} failed`);
console.log('═══════════════════════════════════════════\n');
process.exit(failed > 0 ? 1 : 0);
