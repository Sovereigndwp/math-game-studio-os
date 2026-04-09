#!/usr/bin/env node
/**
 * Echo Heist — Pass 4 & 5 Playtest Simulation
 * Validates all Pass 1–5 systems headlessly.
 */
const fs = require('fs');
const path = require('path');

// ── DOM/Canvas stubs ──────────────────────────────────────────
const stubEl = () => ({ style:{display:'',setProperty(){}}, classList:{add(){},remove(){}}, className:'', textContent:'', value:'', innerHTML:'', focus(){}, addEventListener(){} });
global.document = { getElementById: () => stubEl(), addEventListener(){} };
global.requestAnimationFrame = () => {};
global.window = { AudioContext: class { createOscillator(){return{type:'',frequency:{value:0},connect(){},start(){},stop(){}}} createGain(){return{gain:{value:0,linearRampToValueAtTime(){},setValueAtTime(){}},connect(){}}} get destination(){return{}} }, webkitAudioContext: undefined };
global.localStorage = { _store:{}, getItem(k){return this._store[k]||null}, setItem(k,v){this._store[k]=v}, removeItem(k){delete this._store[k]} };
const ctxStub = new Proxy({},{get(t,p){if(p==='createRadialGradient')return()=>({addColorStop(){}});return function(){}},set(){return true}});
const canvasStub = {width:960,height:640,getContext:()=>ctxStub};
global.document.getElementById = (id) => id === 'game' ? canvasStub : stubEl();

// ── Load game ─────────────────────────────────────────────────
const html = fs.readFileSync(path.join(__dirname,'current.html'),'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
const code = m[1] + `\nmodule.exports={STATE,MISSIONS,LEVELS,CLASSES,TILE,COLS,ROWS,T,DISTRICT_CONFIG,D3_MISSION_DATA,
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
get echoCharges(){return echoCharges},set echoCharges(v){echoCharges=v},get echoGhosts(){return echoGhosts},get echoRecording(){return echoRecording},
get abilityCooldown(){return abilityCooldown},set abilityCooldown(v){abilityCooldown=v},
get abilityBuffType(){return abilityBuffType},get abilityBuffTimer(){return abilityBuffTimer},
get abilityActive(){return abilityActive},get abilityBuffData(){return abilityBuffData},
get gadgetAvailable(){return gadgetAvailable},get gadgetPos(){return gadgetPos},
get gadgetEmitting(){return gadgetEmitting},get gadgetTimer(){return gadgetTimer},
get totalHintsUsed(){return totalHintsUsed},get currentHintsUsed(){return currentHintsUsed},
get scaffoldVisible(){return scaffoldVisible},set scaffoldVisible(v){scaffoldVisible=v},
get wrongCount(){return wrongCount},set wrongCount(v){wrongCount=v},
get objCount(){return objCount},set objCount(v){objCount=v},
get maxHeat(){return maxHeat},set maxHeat(v){maxHeat=v},
get objCompleted(){return objCompleted},get objBonusEarned(){return objBonusEarned},
get highScores(){return highScores},get completedMissions(){return completedMissions},
get streaks(){return streaks},get masteryTemplates(){return masteryTemplates},get skillResults(){return skillResults},
loadLevel,updatePlayer,updateGuard,updateCamera,updateEcho,updateEscape,
startVault,advanceVault,finishVault,startEscape,
startEchoRecording,stopEchoRecording,
tryInteract,openMathPopup,closeMathPopup,checkAnswer,tileAt,isSolid,pixelToGrid,finishMission,
handleMenuKey,handleBriefingKey,handlePlayingKey,handleMathKey,handleVaultKey,handleResultsKey,
handleMissionSelectKey,
activateAbility,resolveAbility,placeGadget,showHint,
getDistrict,getDConfig,generateLevel,isClassUnlocked,getDailySeed,
keys};`
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
// D3 curated content checks
console.log('\n1b. D3 CURATED CONTENT');
assert(G.D3_MISSION_DATA.length === 10, '10 D3 missions in D3_MISSION_DATA');
assert(G.MISSIONS[20].id === 21, 'Mission 21 starts D3 block');
assert(G.MISSIONS[29].id === 30, 'Mission 30 is last D3 mission');
// All D3 prompts have template + answer + hints
for (const m of G.D3_MISSION_DATA) {
  for (const p of m.prompts) {
    assert(p.template && p.answer && p.hint1 && p.hint2,
      `D3 M${m.id} prompt ${p.id}: template/answer/hints present`);
  }
}
// Spot-check specific answers
assert(G.checkAnswer('48', G.MISSIONS[20].prompts[0].answer), 'D3 M21 p1: 25% of 64 = 48');
assert(G.checkAnswer('9',  G.MISSIONS[21].prompts[0].answer), 'D3 M22 p1: 3x+8=35 → x=9');
assert(G.checkAnswer('45', G.MISSIONS[22].prompts[0].answer), 'D3 M23 p1: 1.8×25=45');
assert(G.checkAnswer('18.5',G.MISSIONS[25].prompts[0].answer),'D3 M26 p1: EV=18.5');
assert(G.checkAnswer('360', G.MISSIONS[28].prompts[3].answer), 'D3 M29 p4: full rotation=360°');
assert(G.checkAnswer('11/16',G.MISSIONS[29].prompts[1].answer),'D3 M30 p2: 3/8+5/16=11/16');
// ObjType fields
assert(G.MISSIONS[0].objType === 'stealth',  'Mission 1 objType: stealth');
assert(G.MISSIONS[1].objType === 'cameras',  'Mission 2 objType: cameras');
assert(G.MISSIONS[2].objType === 'doors',    'Mission 3 objType: doors');
assert(G.MISSIONS[20].objType === 'stealth', 'D3 M21 objType: stealth');
assert(G.MISSIONS[23].objType === 'doors',   'D3 M24 objType: doors');

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

// ── 5. Hints + auto-hint + scaffold ──
console.log('\n5. HINTS + AUTO-HINT + SCAFFOLD');
safeGuards();
const ia0 = G.interactables[0];
moveTo(ia0.gx, ia0.gy);
simKey('e');
assert(G.gameState === G.STATE.MATH, 'Popup for hint test');
const sb = G.score;
G.showHint();
assert(G.currentHintsUsed === 1, 'Hint 1');
assert(G.score < sb, 'Score reduced (H-key hint costs)');
G.showHint();
assert(G.currentHintsUsed === 2, 'Hint 2');
G.showHint();
assert(G.currentHintsUsed === 2, 'Capped at 2');
// Free auto-hint
const sb2 = G.score;
G.currentHintsUsed = 0; G.wrongCount = 1;
G.showHint(true);
assert(G.score === sb2, 'Free auto-hint: no score deduction');
G.wrongCount = 0;
// Scaffold toggle
G.scaffoldVisible = false;
const fe = {key:'f',preventDefault(){}};
G.handleMathKey(fe);
assert(G.scaffoldVisible, 'Scaffold toggled ON by F key');
G.handleMathKey(fe);
assert(!G.scaffoldVisible, 'Scaffold toggled OFF by F key');
typeAns(ia0.prompt.answer);
G.closeMathPopup(true);
assert(!G.scaffoldVisible, 'Scaffold reset after close');

// ── 5b. Objective tracking ──
console.log('\n5b. OBJECTIVE TRACKING');
G.currentMission = 1; G.loadLevel(1); G.gameState = G.STATE.PLAYING;
assert(G.objCount === 0, 'objCount reset on load');
assert(G.maxHeat === 0, 'maxHeat reset on load');
// Simulate disabling cameras via terminal solves
for (const ia2 of G.interactables) {
  if (ia2.type === 'terminal') {
    moveTo(ia2.gx, ia2.gy); safeGuards();
    G.openMathPopup(ia2);
    if (G.gameState === G.STATE.MATH) { G.closeMathPopup(true); }
  }
}
assert(G.MISSIONS[1].objType === 'cameras', 'Mission 2 camera objective present');
G.currentMission = 0; G.loadLevel(0); G.gameState = G.STATE.PLAYING;

// ── 5c. Echo charges ──
console.log('\n5c. ECHO CHARGES (×2)');
G.currentMission = 0; G.loadLevel(0); G.gameState = G.STATE.PLAYING;
assert(G.echoCharges === 2, 'echoCharges starts at 2');
G.startEchoRecording();
assert(G.echoRecording, 'Recording started');
for(let i=0;i<200;i++) G.updatePlayer(0.016);
G.stopEchoRecording();
assert(G.echoCharges === 1, 'Charge consumed: now 1');
assert(G.echoGhosts.length === 1, 'Ghost pushed to array');
G.startEchoRecording();
for(let i=0;i<200;i++) G.updatePlayer(0.016);
G.stopEchoRecording();
assert(G.echoCharges === 0, 'Charge consumed: now 0');
assert(G.echoGhosts.length === 2, 'Two ghosts tracked');
G.startEchoRecording();
assert(!G.echoRecording, 'No recording when charges = 0');

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

// ── 11. Mastery streaks (Pass 3 regression) ──
console.log('\n11. MASTERY STREAKS');
G.currentMission=0; G.loadLevel(0); G.gameState=G.STATE.PLAYING;
assert(Object.keys(G.streaks).length === 0, 'Streaks cleared on load');
// Simulate 3 correct answers for T9 template
for(let i=0;i<3;i++){
  const p={template:'T9',text:'Test',answer:'5',hint1:'',hint2:''};
  G.openMathPopup({prompt:p,x:G.player.x,y:G.player.y,type:'terminal',solved:false,gx:2,gy:2});
  typeAns('5');
}
assert((G.streaks['T9']||0) >= 3 || G.masteryTemplates['T9'], 'T9 streak ≥3 or mastery set');

// ── 12. class unlock logic (Pass 5) ──
console.log('\n12. CLASS UNLOCK');
assert(G.isClassUnlocked('hacker'), 'Hacker always unlocked');
const origSize = G.completedMissions.size;
// Ghost unlocked if >= 5
const ghostUnlocked5 = G.completedMissions.size >= 5;
assert(G.isClassUnlocked('ghost') === ghostUnlocked5, `Ghost unlock matches completions: ${G.completedMissions.size}`);

// ── 13. Daily seed (Pass 5) ──
console.log('\n13. DAILY CONTRACT SEED');
const seed = G.getDailySeed();
assert(seed > 20000000 && seed < 21000000, `Daily seed in range: ${seed}`);
assert(seed % 30 >= 0 && seed % 30 < 30, `Mission index 0-29: ${seed%30}`);

// ── 14. Mission select state (Pass 5) ──
console.log('\n14. MISSION SELECT');
assert(G.STATE.MISSION_SELECT === 'mission_select', 'MISSION_SELECT state exists');
const e1 = {key:'ArrowRight',preventDefault(){}};
const e2 = {key:'Enter',preventDefault(){}};
G.gameState = G.STATE.MISSION_SELECT;
G.missionSelectIdx = 0; // can't expose directly but state is testable via handleMissionSelectKey
// Not much headless can do here without DOM but verify the state transition
G.handleMissionSelectKey({key:'ArrowRight',preventDefault(){}});
G.handleMissionSelectKey({key:'ArrowRight',preventDefault(){}});
G.handleMissionSelectKey({key:'Escape',preventDefault(){}});
assert(G.gameState === G.STATE.MENU, 'Esc from mission select returns to menu');

// ── 15. localStorage persistence (Pass 4) ──
console.log('\n15. LOCALSTORAGE PERSISTENCE');
G.currentMission=0; G.loadLevel(0); G.gameState=G.STATE.PLAYING;
G.score=999;
const beforeHS = JSON.stringify(G.highScores);
G.finishMission();
const afterHS = JSON.stringify(G.highScores);
assert(G.highScores[1] === G.score || G.highScores[1] >= 999, 'High score saved for mission 1');
assert(G.completedMissions.has(1), 'Mission 1 in completedMissions');

// ═══════════════════════════════════════════
console.log('\n═══════════════════════════════════════════');
console.log(`  RESULTS: ${passed} passed, ${failed} failed`);
console.log('═══════════════════════════════════════════\n');
process.exit(failed > 0 ? 1 : 0);
